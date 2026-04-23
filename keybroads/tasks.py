from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
)
from crud import task_crud


async def tasks(session: AsyncSession, user_id: int) -> InlineKeyboardMarkup | None:
    """
    Return an inline keyboard with user tasks.
    """
    user_tasks = await task_crud.get_multi(db=session, user_id=user_id)
    if not user_tasks:
        return None

    keyboard = InlineKeyboardBuilder()
    for task in user_tasks:
        keyboard.add(InlineKeyboardButton(text=task.title, callback_data=f'task_{task.id}'))
    return keyboard.adjust(1).as_markup()
