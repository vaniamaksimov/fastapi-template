from http import HTTPStatus
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.session import Session


async def test_client_get_sessions(
    auth_client: AsyncClient, another_user_session: Session
):
    response = await auth_client.get('/api/v1/session')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert response_data[0].get('id')
    assert response_data[0].get('created_at')
    assert len(response_data) == 1


async def test_not_auth_client_get_sessions(client: AsyncClient):
    response = await client.get('/api/v1/session')
    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_client_delete_its_session(
    auth_client: AsyncClient, session: AsyncSession
):
    response = await auth_client.delete('api/v1/session/1')
    assert response.status_code == HTTPStatus.OK
    sessions = (await session.execute(select(Session))).scalars().all()
    assert not sessions


async def test_client_delete_not_its_session(
    auth_client: AsyncClient, session: AsyncSession, another_user_session: Session
):
    sessions_count_before = len(
        (await session.execute(select(Session))).scalars().all()
    )
    response = await auth_client.delete(f'/api/v1/session/{another_user_session.id}')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    session_count_after = len((await session.execute(select(Session))).scalars().all())
    assert sessions_count_before == session_count_after
