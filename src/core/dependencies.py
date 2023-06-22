from http import HTTPStatus
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.managers.session import SessionManager

from src.managers.user import UserManager
from src.models.user import User
from src.schemas.token import TokenData

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


async def authenticate(bearer_token: str = Depends(oauth2bearer)):
    if bearer_token:
        ...
    raise


async def current_user(
    token_data: TokenData = Depends(authenticate),
    user_manager: UserManager = Depends(UserManager),
):
    user = await user_manager.get(id=token_data.user_id)
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
