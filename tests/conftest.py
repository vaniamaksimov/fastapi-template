import asyncio
from copy import deepcopy

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, create_async_engine
from src.core.database import Base

from src.core.dependencies import get_async_session
from src.main import app
from src.models.user import User
from src.utils import password_helper
from tests.factories.user_factory import UserFactory

pytest_plugins = [
    'tests.fixtures.password_helper_fixtures',
    'tests.fixtures.crud_fixtures',
    'tests.fixtures.manager_fixtures',
]


@pytest.fixture
async def engine():
    return create_async_engine(url='sqlite+aiosqlite:///./test_fastapi.db')


@pytest.fixture(scope='session', autouse=True)
async def create_db():
    engine = create_async_engine(url='sqlite+aiosqlite:///./test_fastapi.db')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def connection(engine):
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


@pytest.fixture
async def test_user(session: AsyncSession):
    user = UserFactory()
    db_user = deepcopy(user)
    db_user.password = password_helper.hash(db_user.password)
    session.add(db_user)
    await session.commit()
    return user


@pytest.fixture
async def auth_client(test_user: User, client: AsyncClient):
    response = await client.post(
        '/api/v1/login',
        data={'username': test_user.email, 'password': test_user.password},
    )
    response_data: dict = response.json()
    token = response_data.get('access_token')
    client.headers.update({'Authorization': f'Bearer {token}'})
    return client
