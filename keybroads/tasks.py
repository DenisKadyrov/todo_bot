from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
)
from crud import task_crud


async def tasks(session: AsyncSession, user_id):
    """
    function that return keyboard with tasks
    """
    tasks = await task_crud.get_multi(db=session, user_id=user_id)
    keyboard = InlineKeyboardBuilder()
    for task in tasks:
        keyboard.add(InlineKeyboardButton(text=task.title, callback_data=f'task_{task.id}'))
    return keyboard.adjust(1).as_markup()
