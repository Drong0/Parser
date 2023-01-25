
from fastapi import FastAPI
import json

app = FastAPI()


@app.get("/smartphones")
def get_smartphones(price: int):
    # Расположил открытие файла внутри функции, чтобы при
    with open('smartphones.json', 'r') as f:
        smartphones_data = json.load(f)

    filtered_data = [s for s in smartphones_data if s['price'] == price]
    return filtered_data
