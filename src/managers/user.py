from http import HTTPStatus
from typing import Any, Coroutine

from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.user import UserCrud, user_crud
from src.managers.session import SessionManager
from src.models.session import Session
from src.models.user import User
from src.schemas.login_response import LoginResponse
from src.schemas.session import SessionCreate
from src.schemas.token import TokenData
from src.schemas.user import UserCreate, UserCreateAdmin, UserUpdate, UserUpdateAdmin
from src.utils.token_helper import token_helper
from src.utils.app_exceptions.manager import ManagerError
from src.utils.password_helper import password_helper

from .base import BaseManager


class UserManager(
    BaseManager[
        User, UserCrud, UserCreate | UserCreateAdmin, UserUpdate | UserUpdateAdmin
    ]
):
    def __init__(
        self,
        session: AsyncSession,
        request: Request | None = None,
        crud: UserCrud = user_crud,
    ) -> None:
        super().__init__(session, request, crud)

    async def _before_create(
        self, schema: UserCreate | UserCreateAdmin
    ) -> Coroutine[Any, Any, UserCreate | UserCreateAdmin]:
        schema.password = password_helper.hash(schema.password)
        return await super()._before_create(schema)

    async def _before_login(self, login_data: OAuth2PasswordRequestForm):
        return login_data

    async def login(
        self, login_data: OAuth2PasswordRequestForm
    ) -> Coroutine[Any, Any, LoginResponse]:
        login_data = await self._before_login(login_data)
        try:
            user = await self.get(email=login_data.username)
        except ManagerError:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Пользователя с такой почтой не зарегистрировано.',
            )
        if not password_helper.verify(
            plain_password=login_data.password, hashed_password=user.password
        ):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Не верный логин или пароль.'
            )
        session = await SessionManager(self.session, self.request).create(
            SessionCreate(user_id=user.id)
        )
        token = token_helper.create(TokenData(sid=session.id))
        await self._after_login(session, token)
        return LoginResponse(access_token=token)

    async def _after_login(self, session: Session, token: str):
        ...
