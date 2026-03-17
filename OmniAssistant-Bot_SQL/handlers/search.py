from aiogram import Router, types
from aiogram.filters import Command
from database import cursor,connect
from youtubesearchpython import VideosSearch 
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, types, F


router = Router()


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


@router.callback_query(F.data == 'save_track')
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


@router.message(Command('check'))
async def cmd_check(message: types.Message):
    user_id = message.from_user.id
    cursor.execute('SELECT track_id, title, link FROM music WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()

    if not rows:
        await message.answer("📭 Твой плейлист пуст!")
        return

    await message.answer("📂 **Твои сохраненные треки:**\n\n")
    for row in rows:
        track_id = row[0]
        title = row[1] # получаем айди каждого элемента 
        link = row[2]

        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text= f'Удалить трек {title}', # создаем кнопку delete
            callback_data= f'del_{track_id}') # передаем айди трека чтобы мы потом могли узнать его в переменной track_id 
            )

        await message.answer(
            'Чтобы удалить трек нажмите на кнопку ниже',
            reply_markup=builder.as_markup()
        )

@router.callback_query(F.data.startswith('del_'))
async def callback_delete(callback: types.CallbackQuery):

    track_id = callback.data.split('_')[1] # берем только айди трека из кнопки  
    user_id = callback.from_user.id

    cursor.execute("DELETE FROM music WHERE track_id = ? AND user_id = ?", (int(track_id), user_id)) # удаляем трек по айди 
    connect.commit()
    
    await callback.answer("Удалено!")
    await callback.message.delete()


@router.message(F.text & ~F.text.startswith('/'))
async def echo_search(message: types.Message):
    # При вводе текста вызываем ПОИСК, а не сохранение
    await search_and_send(message, message.text)
