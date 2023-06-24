from http import HTTPStatus
from typing import Any, Coroutine

from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.session import SessionCrud, session_crud
from src.managers.base import BaseManager
from src.models.session import Session
from src.schemas.session import SessionCreate, SessionUpdate


class SessionManager(BaseManager[Session, SessionCrud, SessionCreate, SessionUpdate]):
    def __init__(
        self,
        session: AsyncSession,
        request: Request | None = None,
        crud: SessionCrud = session_crud,
    ) -> None:
        super().__init__(session, request, crud)

    async def _before_remove(self, session: Session) -> Coroutine[Any, Any, None]:
        if (
            await session.awaitable_attrs.user
        ) != self.request.state.user and not self.request.state.user.is_superuser:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail='Недостаточно прав.'
            )
        return await super()._before_remove(session)
