from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_async_session
from datetime import datetime, timedelta
from loguru import logger

router = APIRouter()


@router.get("/stats/{user_id}/today")
async def get_today_stats(
    user_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    from sqlalchemy import text
    today = datetime.utcnow().date()
    
    result = await session.execute(
        text("""
            SELECT game_id, SUM(duration_minutes) as total_minutes
            FROM game_sessions
            WHERE user_id = :user_id
            AND DATE(started_at) = :today
            AND ended_at IS NOT NULL
            GROUP BY game_id
            ORDER BY total_minutes DESC
        """),
        {"user_id": user_id, "today": today}
    )
    rows = result.fetchall()
    
    stats = [
        {"game_id": row.game_id, "total_minutes": row.total_minutes}
        for row in rows
    ]
    total = sum(row.total_minutes for row in rows)
    
    return {
        "user_id": user_id,
        "date": str(today),
        "games": stats,
        "total_minutes": total
    }


@router.get("/stats/{user_id}/week")
async def get_week_stats(
    user_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    from sqlalchemy import text
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    result = await session.execute(
        text("""
            SELECT game_id, SUM(duration_minutes) as total_minutes
            FROM game_sessions
            WHERE user_id = :user_id
            AND started_at >= :week_ago
            AND ended_at IS NOT NULL
            GROUP BY game_id
            ORDER BY total_minutes DESC
        """),
        {"user_id": user_id, "week_ago": week_ago}
    )
    rows = result.fetchall()
    
    stats = [
        {"game_id": row.game_id, "total_minutes": row.total_minutes}
        for row in rows
    ]
    total = sum(row.total_minutes for row in rows)
    
    return {
        "user_id": user_id,
        "period": "7 days",
        "games": stats,
        "total_minutes": total
    }