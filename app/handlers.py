from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from app.keyboards import get_number, registration, help_categories
from .states import Register

router = Router()


@router.message(CommandStart())
async def get_message(message: types.Message):
    await message.answer('👋 Здравствуйте! Я Ваш бот-помощник!\n'
                         'Для создания обращения требуется предоставить\n'
                         'некоторую информацию о себе (кнопка ниже)', reply_markup=registration)


# @router.message(F.text == 'Регистрация')
# async def register(message: types.Message, state: FSMContext):
#     await state.set_state(Register.surname)
#     await message.answer('Введите Вашу Фамилию: ')
#
#
# @router.message(Register.surname)
# async def register_surname(message: types.Message, state: FSMContext):
#     await state.update_data(surname=message.text)
#     await state.set_state(Register.name)
#     await message.answer('Введите Ваше Имя: ')
#
#
# @router.message(Register.name)
# async def register_name(message: types.Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await state.set_state(Register.parent_name)
#     await message.answer('Введите Ваше Отчество: ')
#
#
# @router.message(Register.parent_name)
# async def register_parent_name(message: types.Message, state: FSMContext):
#     await state.update_data(parent_name=message.text)
#     await state.set_state(Register.birthday_date)
#     await message.answer('Введите Вашу дату рождения (образец: 01.01.1991): ')
#
#
# @router.message(Register.birthday_date)
# async def register_birthday_date(message: types.Message, state: FSMContext):
#     await state.update_data(birthday_date=message.text)
#     await state.set_state(Register.phone_number)
#     await message.answer('Нажмите на кнопку ниже, чтобы предоставить Ваш контактный номер телефона: ', reply_markup=get_number)
#
#
# @router.message(Register.phone_number, F.contact)
# async def register_number(message: types.Message, state: FSMContext):
#     await state.update_data(phone_number=message.contact.phone_number)
#     await state.set_state(Register.help_category)
#     await message.answer('Выберите одну из категорий: ', reply_markup=help_categories)
#
#
# @router.message(Register.help_category)
# async def register_help_category(message: types.Message, state: FSMContext):
#     await state.update_data(help_category=message.text)
#     data = await state.get_data()
#     await message.answer(f'Ваша Фамилия: {data["surname"]}\n'
#                          f'Ваше Имя: {data["name"]}\n'
#                          f'Ваше Отчество: {data["parent_name"]}\n'
#                          f'Ваша дата рождения: {data["birthday_date"]}\n'
#                          f'Номер телефона: {data["phone_number"]}\n'
#                          f'Категория: {data["help_category"]}'
#                          )
#     await state.clear()
