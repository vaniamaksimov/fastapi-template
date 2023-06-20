from sqlalchemy.ext.asyncio import AsyncSession

from .database import AsyncSessionLocal


async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as async_session:
        yield async_session
