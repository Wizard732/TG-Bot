import sqlite3

connect = sqlite3.connect('main.db')
cursor = connect.cursor()

import sqlite3

# 1. Создаем соединение
connect = sqlite3.connect('main.db')
cursor = connect.cursor()

# 2. Функция, которая просто готовит таблицы
def create_db():
    # Пользователи
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        user_name TEXT,
        requests INTEGER DEFAULT 0 
    )""")

    # Музыка
    cursor.execute("""CREATE TABLE IF NOT EXISTS music(
        track_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT, 
        link TEXT
    )""")

    # Вес
    cursor.execute("""CREATE TABLE IF NOT EXISTS weight(
        data TEXT,
        weight FLOAT,
        users_id INTEGER
    )""")
    connect.commit()

# Запускаем создание при старте
create_db()