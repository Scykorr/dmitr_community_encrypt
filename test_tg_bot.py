
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
import os
from dotenv import load_dotenv

# # Загрузка переменных окружения
# load_dotenv()

# # Инициализация бота и диспетчера
# bot = Bot(token=os.getenv("TOKEN"))
# dp = Dispatcher()

# # Словарь для хранения файлов пользователей
# user_files = {}

# # Команда /start


# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer("Привет! Отправь мне файл, и я отправлю его другому пользователю.")

# # Обработка документов


# @dp.message()
# async def handle_document(message: types.Message):
#     if message.document:
#         # Сохраняем file_id файла
#         user_files[message.from_user.id] = message.document.file_id
#         await message.answer("Файл получен. Теперь отправь мне username пользователя, которому нужно отправить файл (например, @username).")
#     elif message.text and message.text.startswith("@"):
#         # Получаем username
#         username = message.text[1:]  # Убираем символ @
#         if message.from_user.id in user_files:
#             file_id = user_files[message.from_user.id]

#             # Пытаемся отправить файл
#             try:
#                 await bot.send_message(chat_id=username, text="Проверка доступности...")
#                 # Если сообщение отправлено, отправляем файл
#                 await bot.send_document(chat_id=username, document=file_id)
#                 await message.answer(f"Файл отправлен пользователю @{username}.")
#             except Exception as e:
#                 await message.answer(f"Не удалось отправить файл. Ошибка: {e}. Убедитесь, что пользователь @{username} начал диалог с ботом.")
#         else:
#             await message.answer("Сначала отправь мне файл.")
#     else:
#         await message.answer("Пожалуйста, отправь мне файл или username пользователя.")

# # Запуск бота


# async def main():
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
######################################################################################

# # Замените на токен вашего бота


load_dotenv()
token = os.getenv('TOKEN')
# Инициализация бота и диспетчера
bot = Bot(token=token)
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


# @dp.message()
# async def handle_document(message: types.Message):
#     if message.document:
#         user_files[message.from_user.id] = message.document.file_id
#         await message.answer("Файл получен. Теперь отправь мне username пользователя, которому нужно отправить файл (например, @username).")
#     elif message.text and message.text.startswith("@"):
#         username = message.text[1:]
#         if message.from_user.id in user_files:
#             file_id = user_files[message.from_user.id]
#             try:
#                 await bot.send_document(chat_id=username, document=file_id)
#                 await message.answer(f"Файл отправлен пользователю @{username}.")
#             except Exception as e:
#                 await message.answer(f"Не удалось отправить файл. Ошибка: {e}")
#         else:
#             await message.answer("Сначала отправь мне файл.")
#     else:
#         await message.answer("Пожалуйста, отправь мне файл или username пользователя.")

# Запуск бота


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
