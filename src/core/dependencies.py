from http import HTTPStatus
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.managers.session import SessionManager

from src.managers.user import UserManager
from src.models.session import Session
from src.models.user import User
from src.utils.app_exceptions.manager import ManagerError
from src.utils.token_helper import token_helper

from .database import AsyncSessionLocal

oauth2bearer = OAuth2PasswordBearer(tokenUrl="api/v1/login", auto_error=False)


async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as async_session:
        yield async_session


async def user_manager(
    request: Request, session: AsyncSession = Depends(get_async_session)
) -> UserManager:
    return UserManager(session, request)


async def session_manager(
    request: Request, session: AsyncSession = Depends(get_async_session)
):
    return SessionManager(session, request)


async def user_session(
    bearer_token: str = Depends(oauth2bearer),
    session_manager: SessionManager = Depends(session_manager),
):
    if bearer_token:
        token_data = token_helper.decode(bearer_token)
        try:
            return await session_manager.get(id=token_data.sid)
        except ManagerError:
            pass
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def current_user(
    user_session: Session = Depends(user_session),
):
    user: User = await user_session.awaitable_attrs.user
    if not user.is_active:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Необходимо подтвердить почту.'
        )
    return user


async def current_superuser(user: User = Depends(current_user)):
    if not user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Недостаточно прав.'
        )
    return user
