import httpx
from loguru import logger
from app.config import settings

TELEGRAM_API_BASE = "https://api.telegram.org"


async def send_message(chat_id: str, text: str) -> bool:
    url = f"{TELEGRAM_API_BASE}/bot{settings.telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if response.status_code == 200:
            logger.info(f"Повідомлення відправлено в {chat_id}")
            return True
        logger.error(f"Помилка відправки: {response.text}")
        return False