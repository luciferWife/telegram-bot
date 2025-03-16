import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
git add .
git commit -m "Перенесла токен в переменные окружения"
git push origin main

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("Регистрация"))

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Добро пожаловать в бота.", reply_markup=main_menu)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
