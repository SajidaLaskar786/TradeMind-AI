

from fastapi import FastAPI
from backend.routers import health

app = FastAPI(title="TradeMind-AI API")

app.include_router(health.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to TradeMind-AI!",
        "status": "running"
    }

