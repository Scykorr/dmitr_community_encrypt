import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

# Замените на токен вашего бота
token = '7724435548:AAG5lix0YKaPjEW2rVuj5Fnn7avFNfGkId4'

# Настройка логирования
logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=token)
    dp = Dispatcher()
    await dp.start_polling(bot)

    @dp.message(Command("start"))
    async def send_welcome(message: types.Message):
        await message.reply("Привет! Я ваш бот. Используйте /help для получения списка команд.")

    @dp.message(Command("help"))
    async def send_help(message: types.Message):
        await message.reply("Доступные команды:\n/start - Приветствие\n/help - Список команд")

    @dp.message(Command("sendfile"))
    async def send_file(message: types.Message):
        file_path = 'path/to/your/file.txt'  # Укажите путь к вашему файлу
        with open(file_path, 'rb') as file:
            await bot.send_document(message.chat.id, file)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
