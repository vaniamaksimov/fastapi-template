from typing import Any, Coroutine
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.user import UserCrud, user_crud
from src.models.user import User
from src.schemas.user import UserCreate, UserCreateAdmin, UserUpdate, UserUpdateAdmin
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
