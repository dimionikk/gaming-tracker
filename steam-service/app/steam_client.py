import httpx
from loguru import logger
from app.config import settings

STEAM_API_BASE = "https://api.steampowered.com"


class SteamClient:
    
    async def get_owned_games(self, steam_id: str) -> list[dict]:
        url = f"{STEAM_API_BASE}/IPlayerService/GetOwnedGames/v1/"
        params = {
            "key": settings.steam_api_key,
            "steamid": steam_id,
            "include_appinfo": True,
            "include_played_free_games": True,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            games = data.get("response", {}).get("games", [])
            logger.info(f"Steam API повернув {len(games)} ігор для {steam_id}")
            return games


steam_client = SteamClient()