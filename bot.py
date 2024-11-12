import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings
from handlers import router
from middlewares import DbSessionMiddleware

# turn on logging
logging.basicConfig(level=logging.INFO)


async def main():
    engine = create_async_engine(
        str(settings.SQLALCHEMY_DATABASE_URI), 
        echo=True,
    )

    sessionmaker = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    # Automatically reply to all callbacks
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.include_routers(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
