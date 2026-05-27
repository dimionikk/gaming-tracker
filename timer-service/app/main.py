from fastapi import FastAPI
from app.routers import limits

app = FastAPI(title="Gaming Tracker - Timer Service")

app.include_router(limits.router, prefix="/timer", tags=["timer"])


@app.get("/health")
async def health():
    return {"status": "ok"}