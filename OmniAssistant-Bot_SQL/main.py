import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from youtubesearchpython import VideosSearch 
import sqlite3
import os
from dotenv import load_dotenv
from aiogram.filters import Command, CommandObject
from datetime import date, datetime

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher() # подключаем бота

connect = sqlite3.connect('main.db')
cursor = connect.cursor() # подключаем sql

# Создаем таблицы
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    user_name TEXT,
    requests INTEGER DEFAULT 0 
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS music(
    user_id INTEGER,
    title TEXT, 
    link TEXT
)""")
connect.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS weight(
    data INTEGER,
    weight FLOAT
)""")
connect.commit()

@dp.message(Command("start"))
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


async def search_and_send(message: types.Message, query: str):
    status_msg = await message.answer(f'🔍 ищу "{query}"...')
    try:
        search = VideosSearch(query, limit=1)
        result = search.result() # делаем поиск по названию и выводим самое похожее 

        if result['result']:
            video = result['result'][0]
            title = video['title']
            link = video['link'] # берем данные с json
            duration = video['duration']

            builder = InlineKeyboardBuilder()
            # ПЕРВАЯ кнопка должна быть с URL, чтобы save_to_db её нашла
            builder.row(
                types.InlineKeyboardButton(text='🎧 Слушать', url=link),
                types.InlineKeyboardButton(text='💾 Сохранить', callback_data='save_track')
            ) # создаем кнопки 
            
            await status_msg.edit_text(
                f"✅ Найдено!\n\n🎵 {title}\n⏱ {duration}",
                reply_markup=builder.as_markup()
            )
        else:
            await status_msg.edit_text("❌ Ничего не нашлось.")
    except Exception as e:
        await status_msg.edit_text(f"Ошибка: {e}")


@dp.callback_query(F.data == 'save_track')
async def save_to_db(callback: types.CallbackQuery):
    try:
        message_text = callback.message.text
        
        # Ищем название трека в тексте сообщения
        track_title = "Неизвестный трек"
        for line in message_text.split('\n'):
            if "🎵" in line:
                track_title = line.replace("🎵", "").strip()

        # Берем ссылку из первой кнопки
        track_link = callback.message.reply_markup.inline_keyboard[0][0].url
        user_id = callback.from_user.id

        cursor.execute("INSERT INTO music (user_id, title, link) VALUES (?, ?, ?)", 
                       (user_id, track_title, track_link))
        connect.commit() # добавляем музыку в плейлист

        await callback.answer("✅ Сохранено!")
        await callback.message.answer(f"Трек «{track_title}» сохранен. Глянь /check")
    except Exception as e:
        await callback.answer("Ошибка при сохранении")


@dp.message(Command('check'))
async def cmd_check(message: types.Message):
    user_id = message.from_user.id
    cursor.execute('SELECT title, link FROM music WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()

    if not rows:
        await message.answer("📭 Твой плейлист пуст!")
        return

    text = "📂 **Твои сохраненные треки:**\n\n"
    for i, row in enumerate(rows, 1):
        text += f"{i}. [{row[0]}]({row[1]})\n" # выводим в более адекватном формате 
    
    await message.answer(text, parse_mode="Markdown", disable_web_page_preview=True)


@dp.message(F.text & ~F.text.startswith('/'))
async def echo_search(message: types.Message):
    # При вводе текста вызываем ПОИСК, а не сохранение
    await search_and_send(message, message.text)


@dp.message(Command('weight')) # Создаем команду weight
async def cmd_weight(message:types.Message, command: CommandObject):

    cmd = await message.answer('Впишите свой вес!') # просим пользователя вписать свой вес 
    today = date.today() # получаем текущую дату

    if command.args:
        weight = float(command.args.strip()) # command.args будет равен весу
        await cmd.edit_text(f'Ваш вес {weight}кг успешно сохранен!')
    
    else:
        await message.answer("Пожалуйста, введите вес после команды.")

    cursor.execute("INSERT INTO weight (data, weight) VALUES (?,?)",
                   (today,weight)) # Вводим данные в таблицу
    
    cursor.execute("SELECT * FROM weight")
    rows = cursor.fetchall() # получаем данные с таблицы
    for row in rows:
        text = f'дата - {row[0]} \n вес - {row[1]}'

    await message.answer(f'Ваши записанные данные;\n {text}') # выводим данные пользователю
        
    
    async def diff_weight():
        cursor.execute("SELECT weight FROM weight ORDER BY rowid DESC LIMIT 2") 
        rows = cursor.fetchall() # берем вес из таблицы только 2 последних только что и перед этим
        
        if (len(rows) > 1):
            current_w = rows[0][0]  # Последний введенный
            previous_w = rows[1][0] # Предпоследний
            diff = round(current_w - previous_w, 2)

            if (diff > 0):
                await message.answer(f'Набор + {diff}кг')

            elif (diff < 0):
                await message.answer(f'Сброс - {diff}кг')

            else: 
                await message.answer('Вес стабилен')

        else:
            await message.answer('Это ваша первая запись, нужно хотя-бы 2.')

    await diff_weight() # вызываем функцию diff



async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())