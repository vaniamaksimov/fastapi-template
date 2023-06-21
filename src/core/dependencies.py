from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.managers.user import UserManager

from .database import AsyncSessionLocal


async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as async_session:
        yield async_session


async def user_manager(
    request: Request, session: AsyncSession = Depends(get_async_session)
) -> UserManager:
    return UserManager(session, request)
