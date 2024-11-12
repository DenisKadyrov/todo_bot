from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.ext.asyncio import AsyncSession

from schemas import (
    CreateTask,
    CreateUser
)
from crud import task_crud, user_crud
from keybroads import tasks as task_keyboard


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
    obj_in = CreateUser(id=user_id, chat_id=chat_id, username=username,)
    try:
        await user_crud.create(db=session, obj_in=obj_in)
    except:
        await message.answer("Hello, again!")

    await message.answer("HI! Welcome! You can add task with help /add command and show all tasks with command /tsk")


@router.message(StateFilter(None), Command("add"))
async def add_task(
    message: Message,
    state: FSMContext,
):
    await state.set_state(TaskStates.task_title)


@router.message(StateFilter(None), Command("tsk"))
async def get_tasks(
    message: Message,
    session: AsyncSession,
):
    user_id = message.from_user.id
    await message.answer("Click to task for complete", reply_markup=await task_keyboard(session, user_id))


@router.message(TaskStates.task_title)
async def get_task_title(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    user_id = message.from_user.id
    title = message.text
    obj_in = CreateTask(
        user_id=user_id, 
        title=title
    )
    try:
        await task_crud.create(db=session, obj_in=obj_in)
    except:
        await message.answer("Are you send /start command?")
    await state.clear()


@router.message()
async def another_message(message: Message):
    await message.answer("I don't know this command. Try again!")

    
@router.callback_query()
async def delete_task(
    callback: CallbackQuery,
    session: AsyncSession
):
    print(callback.from_user.id)
    await task_crud.remove(db=session, id=callback.data.split('_')[1])
    await callback.message.delete() 
    await callback.message.answer("Click to task for complete", reply_markup= await task_keyboard(session, callback.from_user.id))
    await session.commit()
