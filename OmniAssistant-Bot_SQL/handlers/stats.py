from aiogram import Router, types
from aiogram.filters import Command
from database import cursor,connect
from datetime import date, datetime
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, types, F


router = Router()

@router.message(Command('weight')) # Создаем команду weight
async def cmd_weight(message:types.Message, command: CommandObject):

    cmd = await message.answer('Впишите свой вес!') # просим пользователя вписать свой вес 
    today = date.today() # получаем текущую дату
    user_id = message.from_user.id # update: добавил запись id пользователя в таблицу 

    try:
        if command.args:
            weight = float(command.args.strip()) # command.args будет равен весу
            await cmd.edit_text(f'Ваш вес {weight}кг успешно сохранен!')
    
        else:
            await message.answer("Пожалуйста, введите вес после команды.")
    except:
        await message.answer('Ошибка! Вводите только цифры.') # если пользователь вводит текст в строке для веса выводим ошибку 

    cursor.execute("INSERT INTO weight (data, weight, users_id) VALUES (?,?,?)",
                   (today,weight,user_id)) # Вводим данные в таблицу
    
    cursor.execute("SELECT * FROM weight")
    rows = cursor.fetchall() # получаем данные с таблицы
    for row in rows:
        todays = f'дата - {row[0]}'
        weight = f'вес - {row[1]}' # берем по отдельности вес и дату для удобства
        user_id = f'id - {row[2]}'


    async def diff_weight():
        cursor.execute("SELECT weight FROM weight ORDER BY rowid DESC LIMIT 2") 
        rows = cursor.fetchall() # берем вес из таблицы только 2 последних только что и перед этим
        
        if (len(rows) > 1):
            current_w = rows[0][0]  # Последний введенный вес
            previous_w = rows[1][0] # Предпоследний вес 
            diff = round(current_w - previous_w, 2)

            if (diff > 0):
                await message.answer(f'{todays}\n {weight}\n набор + {diff}кг')

            elif (diff < 0):
                await message.answer(f'{todays}\n {weight}\n сброс - {diff}кг')

            else: 
                await message.answer(f'{todays}\n {weight}\n вес стабилен') # выводим вес, дату, и набор или сброс

        else:
            await message.answer('Это ваша первая запись, нужно хотя-бы 2.')

    await diff_weight() # вызываем функцию diff

    async def general_information_weight():
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text= 'Общая информация о весе',
            callback_data= 'общая информация о весе' # кнопка которая покажет общую статистику
        ))

        await message.answer(
            'Нажмите на кнопку ниже для\n просмотра общей статистику веса',
            reply_markup=builder.as_markup() # текст над кнопкой
        )
    await general_information_weight() 

@router.callback_query(F.data == 'общая информация о весе')
async def callback_info(callback: types.CallbackQuery,):
    user_id = callback.from_user.id

    cursor.execute("SELECT data, weight FROM weight WHERE users_id = ? ORDER BY rowid DESC LIMIT 1", (user_id,))
    row = cursor.fetchone()

    if (row):
        await callback.message.answer(
            f'Общая статистика:\n\n айди - {user_id}\n дата - {row[0]}\n вес - {row[1]}\n' # Если пользователь нажал на кнопку выводим статистику
        )
    else:
        await callback.message.answer('У вас пока что нету записей о весе.')

    await callback.answer()