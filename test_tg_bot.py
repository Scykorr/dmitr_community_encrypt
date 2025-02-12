# Замените на токен вашего бота


import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode


# Инициализация бота и диспетчера
bot = Bot(token='7724435548:AAG5lix0YKaPjEW2rVuj5Fnn7avFNfGkId4')
dp = Dispatcher()

# Словарь для хранения файлов пользователей
user_files = {}

# Команда /start


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Отправь мне файл, и я сохраню его. Затем ты сможешь отправить его другому пользователю по его ID.")

# Обработка документов


@dp.message()
async def handle_document(message: types.Message):
    if message.document:
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path

        # Скачиваем файл
        downloaded_file = await bot.download_file(file_path)

        # Сохраняем файл локально
        file_name = f"downloaded_{message.document.file_name}"
        with open(file_name, "wb") as new_file:
            new_file.write(downloaded_file.read())

        # Сохраняем информацию о файле в словаре
        user_files[message.from_user.id] = file_name

        await message.answer(f"Файл сохранен. Теперь отправь мне ID пользователя, которому хочешь отправить этот файл.")
    elif message.text and message.text.isdigit():
        # Если сообщение является числом (ID пользователя)
        user_id = int(message.text)
        # test_user_id = 1017643795
        # test_chat_id = 1017643795
        # my_id = 1032364685
        if message.from_user.id in user_files:
            file_name = user_files[message.from_user.id]

            # Отправляем файл другому пользователю
            await bot.send_document(user_id, FSInputFile(file_name))
            await message.answer(f"Файл отправлен пользователю с ID {user_id}.")
        else:
            await message.answer("Сначала отправь мне файл.")
    else:
        await message.answer("Пожалуйста, отправь мне файл или ID пользователя.")

# Запуск бота


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
