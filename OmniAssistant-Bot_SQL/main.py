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

from handlers.start import router as cmd_start
from handlers.search import router as search
from handlers.stats import router as weight
from handlers.command import router as command

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN') # подключаем токен бота

connect = sqlite3.connect('main.db')
cursor = connect.cursor() # подключаем sql


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher() # подключаем бота

    dp.include_router(cmd_start) # говорим деспетчеру использовать этот роутер
    dp.include_router(search)
    dp.include_router(weight)
    dp.include_router(command)

    print("Бот запущен!")
    await dp.start_polling(bot) # запускаем бота

if __name__ == "__main__":
    asyncio.run(main())
