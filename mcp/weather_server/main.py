from fastapi import FastAPI
from weather_api import get_weather

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Weather API Server is Running!"}

@app.get("/weather/{city}")
def weather(city: str):
    return get_weather(city)