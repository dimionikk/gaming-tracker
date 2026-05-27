from fastapi import FastAPI
from app.routers import notifications

app = FastAPI(title="Gaming Tracker - Notification Service")

app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])


@app.get("/health")
async def health():
    return {"status": "ok"}