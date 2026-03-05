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
    user_name TEXT,
    requests INTEGER DEFAULT 0 
) 
""") # счетчик по умолчанию равен 0

connect.commit() 

# Этот блок отвечает на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

     # если пользователь есть прибавляем +1 к его requests если нет создаем с 1
    cursor.execute("""
        INSERT INTO users (id, user_name, requests) 
        VALUES (?, ?, 1)
        ON CONFLICT(id) DO UPDATE SET requests = requests + 1
    """, (user_id, user_name)) # Если такой пользователь уже есть прибавляем 1 к его счетчику 
    connect.commit()

    # Получаем текущее значение из базы для вывода
    cursor.execute("SELECT requests FROM users WHERE id = ?", (user_id,)) # Берем обновленное число
    user_count = cursor.fetchone()[0] # достаем число

    await message.answer(
        f"{user_name}, я твой музыкальный бот! 🎸\n"
        f"Ты обратился ко мне уже {user_count}-й раз!"
    )



@dp.message()
async def message_bot(message: types.Message):
    cursor.execute("UPDATE users SET requests = requests + 1 WHERE id = ?", (message.from_user.id,))
    connect.commit()
    
    await message.answer(f'Команда не определена. Выбери нужную команду.')


async def main():
    print("Бот запущен! Проверь его в Telegram.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())




