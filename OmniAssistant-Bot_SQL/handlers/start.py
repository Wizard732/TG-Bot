from aiogram import Router, types
from aiogram.filters import Command
from database import cursor,connect

router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    cursor.execute("""
        INSERT INTO users (id, user_name, requests) 
        VALUES (?, ?, 1)
        ON CONFLICT(id) DO UPDATE SET requests = requests + 1
    """, (user_id, user_name))
    connect.commit() # добавляем айди, ник, и количество запросов

    cursor.execute("SELECT requests FROM users WHERE id = ?", (user_id,))
    user_count = cursor.fetchone()[0]

    await message.answer(
        f"{user_name}, я твой музыкальный бот! 🎸\n"
        f"Ты обратился ко мне уже {user_count}-й раз!"
    )
