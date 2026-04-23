import logging

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import (
    CreateTask,
    CreateUser
)
from crud import task_crud, user_crud
from keybroads import tasks as task_keyboard


logger = logging.getLogger(__name__)


class TaskStates(StatesGroup):
    task_title = State()


router = Router()


@router.message(Command("start"))
async def cmd_start(
    message: Message, 
    session: AsyncSession,
):
    user_id = message.from_user.id
    chat_id = str(message.chat.id)
    username = message.from_user.username
    obj_in = CreateUser(id=user_id, chat_id=chat_id, username=username)

    if await user_crud.get(db=session, id=user_id):
        await message.answer("Hello, again!")
    else:
        try:
            await user_crud.create(db=session, obj_in=obj_in)
        except IntegrityError:
            await session.rollback()
            logger.info("User %s already exists", user_id)
            await message.answer("Hello, again!")
        except Exception:
            await session.rollback()
            logger.exception("Failed to create user %s", user_id)
            await message.answer("Something went wrong. Please try /start again later.")
            return

    await message.answer("HI! Welcome! You can add task with help /add command and show all tasks with command /tsk")


@router.message(StateFilter(None), Command("add"))
async def add_task(
    message: Message,
    state: FSMContext,
):
    await state.set_state(TaskStates.task_title)
    await message.answer("Send me the task title.")


@router.message(StateFilter(None), Command("tsk"))
async def get_tasks(
    message: Message,
    session: AsyncSession,
):
    user_id = message.from_user.id
    keyboard = await task_keyboard(session, user_id)
    if keyboard is None:
        await message.answer("Task list is empty. Add a task with /add.")
        return

    await message.answer("Click a task to complete it.", reply_markup=keyboard)


@router.message(Command("cancel"))
async def cancel_task_input(
    message: Message,
    state: FSMContext,
):
    await state.clear()
    await message.answer("Cancelled.")


@router.message(TaskStates.task_title)
async def get_task_title(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    user_id = message.from_user.id
    title = (message.text or "").strip()
    if not title:
        await message.answer("Task title cannot be empty. Send a text title or /cancel.")
        return

    obj_in = CreateTask(user_id=user_id, title=title)
    try:
        await task_crud.create(db=session, obj_in=obj_in)
    except IntegrityError:
        await session.rollback()
        await message.answer("Please send /start before adding tasks.")
        return
    except Exception:
        await session.rollback()
        logger.exception("Failed to create task for user %s", user_id)
        await message.answer("Something went wrong. Please try again later.")
        return

    await state.clear()
    await message.answer("Task added.")


@router.message()
async def another_message(message: Message):
    await message.answer("I don't know this command. Try again!")

    
@router.callback_query(F.data.startswith("task_"))
async def delete_task(
    callback: CallbackQuery,
    session: AsyncSession
):
    data = callback.data or ""
    try:
        task_id = int(data.removeprefix("task_"))
    except ValueError:
        await callback.answer("Invalid task data.", show_alert=True)
        return

    try:
        deleted = await task_crud.remove(
            db=session,
            id=task_id,
            user_id=callback.from_user.id,
        )
    except Exception:
        await session.rollback()
        logger.exception("Failed to delete task %s", task_id)
        await callback.answer("Something went wrong. Please try again.", show_alert=True)
        return

    if not deleted:
        await callback.answer("Task not found.", show_alert=True)
        return

    if isinstance(callback.message, Message):
        await callback.message.delete()
        keyboard = await task_keyboard(session, callback.from_user.id)
        if keyboard is None:
            await callback.message.answer("All tasks are completed.")
        else:
            await callback.message.answer("Click a task to complete it.", reply_markup=keyboard)
    else:
        await callback.answer("Task completed.")
