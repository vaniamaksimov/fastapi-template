from fastapi import Request
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
