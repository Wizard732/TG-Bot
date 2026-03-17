from aiogram import Router, types
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types, F

router = Router()

@router.message(Command('help')) # создаем команду help
async def cmd_help(message:types.Message):

    button1 = types.InlineKeyboardButton(text="🛠 Список команд", callback_data="command")
    keyboard1 = types.InlineKeyboardMarkup(inline_keyboard=[[button1]]) # создаю кнопку для списка команд 

    await message.answer(
        'Раздел помощь.',
        reply_markup=keyboard1 # выводим кнопку
    )

@router.callback_query(F.data == 'command') # если кнопка command была нажата выводим эти кнопки
async def help_commands(callback:types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=
        [[types.InlineKeyboardButton(text="/Start", callback_data="start")],
        [types.InlineKeyboardButton(text="/Weight", callback_data="weight")], # вложенные кнопки
        [types.InlineKeyboardButton(text="/Check", callback_data="check")]])


    await callback.message.edit_text("Выберите команду:",
         reply_markup=keyboard # выводим кнопки
         )

@router.callback_query(F.data == 'start') # если кнопка start была нажата выводим эту информацию о ней
async def help_start(callback:types.CallbackQuery): 
    await callback.message.answer('Команда (start) используется для\n записи данных пользователя в базу данных.')
    
@router.callback_query(F.data == 'weight') # если кнопка start была нажата выводим эту информацию о ней
async def help_weight(callback:types.CallbackQuery): 
    await callback.message.answer('Команда (weight) ипользуется для\n записи веса пользователя, а так-же выводит его прогресс.')

@router.callback_query(F.data == 'check') # если кнопка start была нажата выводим эту информацию о ней
async def help_check(callback:types.CallbackQuery): 
    await callback.message.answer('Команда (check) используется для\n добавления музыки в плейлист и удаления ее оттуда.')
