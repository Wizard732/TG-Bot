import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from youtubesearchpython import VideosSearch 
import sqlite3
import os
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher() # Подключаем asyncio

connect = sqlite3.connect('main.db')
cursor = connect.cursor() # Подключаем sql

# Создаем таблицу 
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    user_name TEXT
) 
""")

connect.commit() 

# Этот блок отвечает на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"{message.from_user.first_name} Я твой музыкальный бот. 🎸\nПришли мне название песни или имя исполнителя!")

    user_id = message.from_user.id
    user_name = message.from_user.first_name

    cursor.execute('INSERT INTO users (id, user_name) VALUES (?,?)',(user_id, user_name))
    connect.commit() # Добавляем данные в скл



async def main():
    print("Бот запущен! Проверь его в Telegram.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())




