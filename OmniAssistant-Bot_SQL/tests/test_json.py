import pytest
import json
import os
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from handlers.clearJson import clear_json_logic


def test_clear_json():
    # 1. Создаем временный файл, чтобы не портить реальную базу
    test_file = 'test_temp.json'
    with open(test_file, 'w') as f:
        json.dump([1, 2, 3], f)  # Кладем туда мусор

    # 2. Запускаем чистку
    result = clear_json_logic(test_file)

    # 3. ПРОВЕРКИ
    assert result is True  # Проверяем, что функция вернула True

    with open(test_file, 'r') as f:
        data = json.load(f)
    assert data == []  # Проверяем, что список стал пустым

    # Удаляем временный файл после теста
    os.remove(test_file)
