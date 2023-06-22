from http import HTTPStatus
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.managers.session import SessionManager

from src.managers.user import UserManager
from src.utils.token_helper import token_helper
from fastapi.security.utils import get_authorization_scheme_param
from .database import AsyncSessionLocal

oauth2bearer = OAuth2PasswordBearer(tokenUrl="api/v1/login", auto_error=False)


async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as async_session:
        yield async_session


async def add_db_session_to_request(
    request: Request, session: AsyncSession = Depends(get_async_session)
):
    request.state.db_session = session


async def add_current_user_to_request(
    request: Request,
):
    authorization = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    request.state.user = None
    request.state.user_session = None
    if authorization and scheme.lower() == "bearer":
        try:
            token_data = token_helper.decode(param)
            user_session = await SessionManager(request.state.db_session, request).get(
                id=token_data.sid
            )
            request.state.user_session = user_session
            request.state.user = await user_session.awaitable_attrs.user
        except HTTPException:
            pass


async def only_authorized(request: Request, bearer_token: str = Depends(oauth2bearer)):
    if not request.state.user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def current_superuser(request: Request):
    if not request.state.user:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Недостаточно прав.'
        )


async def user_manager(request: Request) -> UserManager:
    return UserManager(request.state.db_session, request)


async def session_manager(request: Request):
    return SessionManager(request.state.db_session, request)
