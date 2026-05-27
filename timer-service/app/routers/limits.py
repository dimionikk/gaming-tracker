from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_async_session
from app.models import GameLimit, GameSession
from app.timer import start_timer, stop_timer, get_elapsed_minutes
from pydantic import BaseModel
from datetime import datetime
from loguru import logger

router = APIRouter()


class LimitCreate(BaseModel):
    user_id: str
    game_id: str
    daily_limit_minutes: int


class SessionStart(BaseModel):
    user_id: str
    game_id: str


@router.post("/limits")
async def create_limit(
    data: LimitCreate,
    session: AsyncSession = Depends(get_async_session)
):
    limit = GameLimit(
        user_id=data.user_id,
        game_id=data.game_id,
        daily_limit_minutes=data.daily_limit_minutes,
    )
    session.add(limit)
    await session.commit()
    return {"message": "Ліміт створено", "limit": data.daily_limit_minutes}


@router.post("/sessions/start")
async def start_session(
    data: SessionStart,
    session: AsyncSession = Depends(get_async_session)
):
    game_session = GameSession(
        user_id=data.user_id,
        game_id=data.game_id,
        started_at=datetime.utcnow(),
    )
    session.add(game_session)
    await session.commit()
    await start_timer(data.user_id, data.game_id)
    return {"message": "Сесію розпочато"}


@router.post("/sessions/stop")
async def stop_session(
    data: SessionStart,
    session: AsyncSession = Depends(get_async_session)
):
    minutes = await stop_timer(data.user_id, data.game_id)
    result = await session.execute(
        select(GameSession)
        .where(GameSession.user_id == data.user_id)
        .where(GameSession.game_id == data.game_id)
        .where(GameSession.ended_at == None)
    )
    game_session = result.scalar_one_or_none()
    if game_session:
        game_session.ended_at = datetime.utcnow()
        game_session.duration_minutes = minutes
        await session.commit()

    return {"message": "Сесію завершено", "duration_minutes": minutes}


@router.get("/sessions/{user_id}/{game_id}/status")
async def get_status(user_id: str, game_id: str, session: AsyncSession = Depends(get_async_session)):
    elapsed = await get_elapsed_minutes(user_id, game_id)
    result = await session.execute(
        select(GameLimit)
        .where(GameLimit.user_id == user_id)
        .where(GameLimit.game_id == game_id)
        .where(GameLimit.is_active == True)
    )
    limit = result.scalar_one_or_none()
    if not limit:
        return {"elapsed_minutes": elapsed, "limit": None}

    remaining = limit.daily_limit_minutes - elapsed
    return {
        "elapsed_minutes": elapsed,
        "limit_minutes": limit.daily_limit_minutes,
        "remaining_minutes": remaining,
        "exceeded": remaining <= 0
    }