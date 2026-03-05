import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from youtubesearchpython import VideosSearch 
# ВСТАВЬ СВОЙ ТОКЕН НИЖЕ
API_TOKEN = 'your_token'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def search_and_send(message: types.Message, query: str): # Создаем функцию которая будет искать песни с ввода текста либо с /find
    """Эта функция умеет только искать и отправлять результат"""
    status_msg = await message.answer(f'{message.from_user.first_name} 🔍 ищу "{query}"...')
    
    try:
        search = VideosSearch(query, limit=1)
        result = search.result() # Получаем результат поиска 

        if result['result']:
            video = result['result'][0]
            title = video['title']
            link = video['link'] # Берем данные с JSON
            duration = video['duration']

            builder = InlineKeyboardBuilder()
            builder.row(types.InlineKeyboardButton(text='🎧 Слушать', url=link)) # Создаем кнопку 
            
            await status_msg.edit_text(
                f"✅ Найдено!\n\n🎵 **{title}**\n⏱ {duration}",
                reply_markup=builder.as_markup() # Сообщение которое получит пользователь если музыка найдена
            )
        else:
            await status_msg.edit_text("❌ Ничего не нашлось.")
    except Exception as e:
        await status_msg.edit_text(f"Ошибка: {e}")


# Этот блок отвечает на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"{message.from_user.first_name} Я твой музыкальный бот. 🎸\nПришли мне название песни или имя исполнителя!")


@dp.message(Command('help'))
async def cmd_help(message: types.Message): # Команда /help
    await message.answer(f'Вы открыли меню помощь! \n {message.from_user.first_name} в чем заключилась проблема?')


@dp.message(Command('about'))
async def cmd_about(message: types.Message):
    await message.answer('Этот бот умеет искать песни по названию либо по имени исполнителя!')


@dp.message(Command('donate'))
async def cmd_donate(message: types.Message):
   status_donate = await message.answer("Задонатить можно тут:")


@dp.message(Command('profile'))
async def cmd_profile(message: types.Message):
       
    builder = InlineKeyboardBuilder()

    builder.row(types.InlineKeyboardButton(
        text = 'Открыть профиль', 
        url =f'tg://user?id={message.from_user.username}') # Создаем кнопку которая перенесет на профиль пользователя
    )
    
    await message.answer(
        'Твой профиль: \n \n'
        f'ID: {message.from_user.id}\n'
        f'User:{message.from_user.first_name}\n', # Выводим сообщения если пользователь вписывает /profile
        reply_markup = builder.as_markup()
    )


# 1. Поиск по команде /find
@dp.message(Command('find'))
async def cmd_find(message: types.Message):
    query = message.text.replace('/find', '').strip()
    if not query:
        await message.answer("Напиши название песни!")
        return
    await search_and_send(message, query)

# 2. Умный поиск (просто текст)
@dp.message(F.text & ~F.text.startswith('/'))
async def echo_search(message: types.Message):
    # Если это не команда (не начинается на /), то просто ищем
    await search_and_send(message, message.text)

  

async def main():
    print("Бот запущен! Проверь его в Telegram.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())