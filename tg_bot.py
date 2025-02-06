"""
t.me/FAStEncryptMsgBot

by Anton Fedosov

"""

import asyncio
from aiogram import Bot, Dispatcher, F
from main_info.token import token
from app.handlers import router
from aiogram.types.input_file import FSInputFile


async def main():
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
