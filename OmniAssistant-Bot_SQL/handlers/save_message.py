from aiogram import Router, types
from aiogram.filters import Command
import json

router = Router()

failname = 'messageUser.json'

@router.message(Command('admin'))
async def save_message(message:types.Message):

    try:
        with open(failname, 'r', encoding='utf-8') as f:
            message_list = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): # если файл не открывается или он пустой создаем список
        message_list = []


    clean_text = message.text.replace('/admin', '').strip() # вырезаем /admin оставляем текст после нее
    if clean_text:
        message_list.append(clean_text)

        with open(failname, 'w', encoding='utf-8') as f:
            json.dump(message_list, f, ensure_ascii=False, indent=4) # записываем текст пользователя в json
        
        await message.answer(f"Сохранено! Теперь в базе {len(message_list)} сообщений.")
        await message.answer(f"Весь список: {message_list}")
    else:
        await message.answer("Напишите что-нибудь после команды /admin")