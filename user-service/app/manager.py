import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from loguru import logger
from app.models import User
from app.database import get_async_session
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings

#відкрити сесію з базою даних юзер і взяти структуру таблиці
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.secret_key
    verification_token_secret = settings.secret_key

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"Юзер {user.email} зареєструвався")

    async def on_after_login(self, user: User, request: Optional[Request] = None, response=None):
        logger.info(f"Юзер {user.email} увійшов")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)