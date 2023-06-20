import asyncio

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from src.core.database import engine
from src.core.dependencies import get_async_session
from src.main import app

pytest_plugins = [
    'tests.fixtures.password_helper_fixtures',
    'tests.fixtures.crud_fixtures',
]


@pytest.fixture
async def connection():
    async with engine.begin() as conn:
        yield conn
        await conn.rollback()


@pytest.fixture
async def session(connection: AsyncConnection):
    async with AsyncSession(bind=connection, expire_on_commit=False) as _session:
        yield _session


@pytest.fixture(autouse=True)
async def override_dependency(session: AsyncSession):
    app.dependency_overrides[get_async_session] = lambda: session


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac, LifespanManager(app):
        yield ac
