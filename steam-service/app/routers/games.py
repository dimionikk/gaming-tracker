from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_async_session
from app.models import Game, UserGame
from app.steam_client import steam_client
from app.cache import get_cached, set_cached, delete_cached
from loguru import logger

router = APIRouter()


@router.get("/games/{steam_id}")
async def get_user_games(
    steam_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    cache_key = f"games:{steam_id}"
    cached = await get_cached(cache_key)
    if cached:
        return {"source": "cache", "games": cached}

    games = await steam_client.get_owned_games(steam_id)

    for game_data in games:
        existing = await session.execute(
            select(Game).where(Game.steam_app_id == game_data["appid"])
        )
        game = existing.scalar_one_or_none()

        if not game:
            game = Game(
                steam_app_id=game_data["appid"],
                name=game_data.get("name", "Unknown"),
                icon_url=game_data.get("img_icon_url"),
            )
            session.add(game)

    await session.commit()
    await set_cached(cache_key, games)

    return {"source": "steam_api", "games": games}


@router.delete("/games/{steam_id}/cache")
async def clear_cache(steam_id: str):
    await delete_cached(f"games:{steam_id}")
    return {"message": "Кеш очищено"}
