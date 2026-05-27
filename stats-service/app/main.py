from fastapi import FastAPI
from app.routers import stats

app = FastAPI(title="Gaming Tracker - Stats Service")

app.include_router(stats.router, prefix="/stats-service", tags=["stats"])


@app.get("/health")
async def health():
    return {"status": "ok"}