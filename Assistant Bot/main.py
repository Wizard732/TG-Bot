import asyncio # Запуск бота
from aiogram import Bot,Dispatcher, types, F # Основа бота
from aiogram.filters import Command # Для того чтобы бот понимал команды
from aiogram.utils.keyboard import InlineKeyboardBuilder # Для кнопок

API_TOKEN = 'your_token'
dp = Dispatcher()
bot = Bot(token=API_TOKEN)
line = 'https://www.google.com/search?q='
count = 0

@dp.message(Command('start'))
async def cmd_help(message:types.Message):
    await message.answer(f'Привет {message.from_user.first_name}! Чем могу помочь?')
    global count
    count += 1 

@dp.message(Command('my_id'))
async def cmd_id(message:types.Message):
    await message.answer(f'{message.from_user.id}')

@dp.message(F.text & ~F.text.startswith('/'))
async def google_search(message: types.Message):
    # Создаем динамическую ссылку: берем основу гугла и приклеиваем текст юзера
    user_query = message.text.replace(" ", "+") # Заменяем пробелы на плюсы для ссылки
    google_link = f"https://www.google.com/search?q={user_query}"

    builder = InlineKeyboardBuilder()
    # Кнопку кладем ВНУТРИ скобок метода row
    builder.row(types.InlineKeyboardButton(
        text="🔍 Найти в Google", 
        url=google_link)
    )
    await message.answer(
        f"Окей, создаю ссылку для поиска: {message.text}",
        reply_markup=builder.as_markup()
        
    )
    global count
    count += 1
        

@dp.message(Command('main'))
async def cmd_main(message: types. Message):

    query = message.text.replace('/main', '').strip()
    link = f"https://www.google.com/search?q={query}"

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text = 'Найти',
        url = link)
    )
    await message.answer(
        f'Ок, создаю ссылку для поиска {message.text}',
        reply_markup=builder.as_markup()
    )
    global count
    count += 1

@dp.message(Command('stats'))
async def cmd_stats(message: types. Message): # Создаем команду статс и выводи пользователю текст
    status = await message.answer(f'{message.from_user.first_name} привет, тут, ты можешь узнать сколько запросов ты ввел!') 

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text = 'Посмотреть статистику запросов.',  # Создаем кнопки 
        callback_data="btn_pressed")
        )

    await status.edit_text(
        f'Нажмите на кнопку ниже чтобы узнать сколько введено запросов',
        reply_markup=builder.as_markup(), # отображение на экране пользователя 
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "btn_pressed")
async def process_callback_stats(callback: types.CallbackQuery): # Если пользователь нажал на кнопку выполняем функцию ниже
    
   await callback.message.edit_text(
        f"📊 *Статистика обновлена!*\n"
        f"Всего введено запросов - *{count}*", # Выводим значение пользователю
        parse_mode="Markdown"
    )
    
    # 2. Отвечаем на колбэк, чтобы кнопка не зависала
   await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
