from http import HTTPStatus

from httpx import AsyncClient
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.session import Session
from src.models.user import User
from src.schemas.user import UserCreate


async def test_client_successful_authenticate(
    client: AsyncClient, test_user: User, session: AsyncSession
):
    user_session = (await session.execute(select(Session))).scalar_one_or_none()
    assert not user_session
    response = await client.post(
        '/api/v1/login',
        data={'username': test_user.email, 'password': test_user.password},
    )
    assert response.status_code == HTTPStatus.OK
    user_session = (await session.execute(select(Session))).scalar_one_or_none()
    assert user_session
    user: User = await user_session.awaitable_attrs.user
    assert user
    assert user.email == test_user.email
    response_data: dict = response.json()
    assert response_data
    assert response_data.get('access_token')
    assert response_data.get('token_type') == 'bearer'


async def test_client_give_invalid_password(
    client: AsyncClient, test_user: User, session: AsyncSession
):
    user_sessions = (await session.execute(select(Session))).scalar_one_or_none()
    assert not user_sessions
    response = await client.post(
        '/api/v1/login',
        data={'username': test_user.email, 'password': test_user.password[::-1]},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    user_session = (await session.execute(select(Session))).scalar_one_or_none()
    assert not user_session
    response_data: dict = response.json()
    assert response_data.get('detail') == 'Не верный логин или пароль.'


async def test_client_give_invalid_email(
    client: AsyncClient, test_user: User, session: AsyncSession
):
    user_sessions = (await session.execute(select(Session))).scalar_one_or_none()
    assert not user_sessions
    response = await client.post(
        '/api/v1/login',
        data={'username': test_user.email[::-1], 'password': test_user.password},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    user_session = (await session.execute(select(Session))).scalar_one_or_none()
    assert not user_session
    response_data: dict = response.json()
    assert (
        response_data.get('detail')
        == 'Пользователя с такой почтой не зарегистрировано.'
    )


async def test_register_new_user(client: AsyncClient, session: AsyncSession):
    users = (await session.execute(select(User))).scalars().all()
    assert not users
    response = await client.post(
        '/api/v1/register',
        json=UserCreate(
            email='email@example.com', password='SomeSuperStrongPassword'
        ).dict(),
    )
    assert response.status_code == HTTPStatus.OK
    user = (await session.execute(select(User))).scalar_one_or_none()
    assert user
    assert user.email == 'email@example.com'
    assert user.password != 'SomeSuperStrongPassword'
    assert not user.first_name
    assert not user.last_name
    assert user.is_active
    assert not user.is_superuser


@pytest.mark.parametrize(
    argnames=['user_json'],
    argvalues=[
        ({'imeil': 'some@email.com', 'password': 'SomeSuperStrongPassword'},),
        ({'email': 'some@email.com', 'passwordss': 'SomeSuperStrongPassword'},),
        ({'email': None, 'password': 'SomeSuperStrongPassword'},),
        ({'email': 'some@email.com', 'password': None},),
    ],
)
async def test_register_new_user_with_bad_data(
    client: AsyncClient, session: AsyncSession, user_json: dict
):
    users = (await session.execute(select(User))).scalars().all()
    assert not users
    response = await client.post('/api/v1/register', json=user_json)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    users = (await session.execute(select(User))).scalars().all()
    assert not users


async def test_client_logged_out(
    auth_client: AsyncClient, session: AsyncSession, test_user: User
):
    user_session = (await session.execute(select(Session))).scalar_one_or_none()
    assert user_session
    user: User = await user_session.awaitable_attrs.user
    assert user.first_name == test_user.first_name
    assert user.email == test_user.email
    response = await auth_client.get('/api/v1/logout')
    assert response.status_code == HTTPStatus.OK
    user_session = (await session.execute(select(Session))).scalar_one_or_none()
    assert not user_session
