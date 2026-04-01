from fastapi import FastAPI
import json
import asyncio

app = FastAPI()

@app.get("/save")
async def save(save: str):
    await asyncio.sleep(3)
    filename = 'messageUser.json'
    data = []

    if (save == "save"): # проверяем что пользователь точно хочет сохранить
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f) # открываем файл читаем и сохраняем в data
                if not isinstance(data, list):
                    data = [] # если в json не список создаем пустой список
        except json.JSONDecodeError:
            data = [] # если в джсон не список создаем список
        return {"message": "File save is successfully"}
    else:
        return {"error": "If you want to save write save"}