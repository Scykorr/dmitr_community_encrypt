from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

registration = get_number = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Отправить файл')]],
    input_field_placeholder='Нажмите на кнопку ниже для отправки файла'
)

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер', request_contact=True)]],
                                 resize_keyboard=True)

help_categories = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Выплата')],
                                                [KeyboardButton(
                                                    text='Эвакуация')],
                                                [KeyboardButton(text='Сертификат')]],
                                      input_field_placeholder='Выберите требуемый пункт меню...')
