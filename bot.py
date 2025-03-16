import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаём бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Главное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("Регистрация"))

# Меню регистрации
registration_menu = ReplyKeyboardMarkup(resize_keyboard=True)
registration_menu.add(KeyboardButton("Соло регистрация"))
registration_menu.add(KeyboardButton("Командная регистрация"))
registration_menu.add(KeyboardButton("🔙 Назад"))

# Словарь для хранения данных пользователей (можно заменить на БД)
user_data = {}

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Добро пожаловать в бота.", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "Регистрация")
async def registration(message: types.Message):
    await message.answer("Выберите тип регистрации:", reply_markup=registration_menu)

@dp.message_handler(lambda message: message.text == "Соло регистрация")
async def solo_registration(message: types.Message):
    await message.answer("Введите ваше имя:")
    user_data[message.from_user.id] = {"type": "solo"}

@dp.message_handler(lambda message: message.text == "Командная регистрация")
async def team_registration(message: types.Message):
    await message.answer("Введите имя капитана команды:")
    user_data[message.from_user.id] = {"type": "team"}

@dp.message_handler(lambda message: message.text == "🔙 Назад")
async def back_to_main(message: types.Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu)

@dp.message_handler()
async def handle_name_or_team(message: types.Message):
    user_id = message.from_user.id

    if user_id in user_data:
        if user_data[user_id]["type"] == "solo" and "name" not in user_data[user_id]:
            user_data[user_id]["name"] = message.text
            await message.answer(f"Соло регистрация завершена! Ваше имя: {message.text}")
            await message.answer("Вы успешно зарегистрированы! Ожидайте связи с администратором.", reply_markup=main_menu)

        elif user_data[user_id]["type"] == "team" and "captain" not in user_data[user_id]:
            user_data[user_id]["captain"] = message.text
            await message.answer("Введите название команды:")

        elif user_data[user_id]["type"] == "team" and "team_name" not in user_data[user_id]:
            user_data[user_id]["team_name"] = message.text
            await message.answer(f"Командная регистрация завершена! Капитан: {user_data[user_id]['captain']}, Команда: {message.text}")
            await message.answer("Вы успешно зарегистрированы! Ожидайте связи с администратором.", reply_markup=main_menu)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
