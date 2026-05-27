from fastapi import APIRouter
from pydantic import BaseModel
from app.telegram import send_message
from loguru import logger

router = APIRouter()


class NotificationRequest(BaseModel):
    chat_id: str
    user_id: str
    game_id: str
    elapsed_minutes: int
    limit_minutes: int


@router.post("/notify/limit-exceeded")
async def notify_limit_exceeded(data: NotificationRequest):
    text = (
        f"⚠️ <b>Ліміт часу вичерпано!</b>\n\n"
        f"🎮 Гра: <b>{data.game_id}</b>\n"
        f"⏱ Зіграно: <b>{data.elapsed_minutes} хв</b>\n"
        f"🚫 Ліміт: <b>{data.limit_minutes} хв</b>\n\n"
        f"Час зробити перерву! 💪"
    )
    success = await send_message(data.chat_id, text)
    if success:
        return {"message": "Сповіщення відправлено"}
    return {"message": "Помилка відправки"}


@router.post("/notify/session-started")
async def notify_session_started(data: NotificationRequest):
    text = (
        f"🎮 <b>Ігрова сесія розпочата</b>\n\n"
        f"Гра: <b>{data.game_id}</b>\n"
        f"Ліміт: <b>{data.limit_minutes} хв</b>\n\n"
        f"Удачі! 🎯"
    )
    success = await send_message(data.chat_id, text)
    if success:
        return {"message": "Сповіщення відправлено"}
    return {"message": "Помилка відправки"}