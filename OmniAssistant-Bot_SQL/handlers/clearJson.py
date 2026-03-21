from aiogram import Router, types
from aiogram.filters import Command
import json

router = Router()

failname = 'messageUser.json'
message_list = []

def clear_json_logic(filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return True
    except Exception:
        return False

@router.message(Command('clear'))
async def clear_list(message:types.Message):
    await message.answer('Воспользуйтесь командой (clear) для очистки списка ')
    try:
        with open(failname, 'w', encoding='utf-8') as f: 
            json.dump(message_list,f) # открываем json файл если там есть записи заменяем их на пустой список

    except (FileNotFoundError, json.JSONDecodeError):
        await message.answer('Ошибка открытия либо записи файла')
    else:
        await message.answer('Данные из списка успешно очищены') # выводим при успешном завершение блока try