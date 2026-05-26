from fastapi import FastAPI
from app.routers import games

app = FastAPI(title="Gaming Tracker - Steam Service")

app.include_router(games.router, prefix="/steam", tags=["steam"])


@app.get("/health")
async def health():
    return {"status": "ok"}