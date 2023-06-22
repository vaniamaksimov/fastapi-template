from src.crud.base import CrudBase
from src.models.session import Session
from src.schemas.session import SessionCreate, SessionUpdate


class SessionCrud(CrudBase[Session, SessionCreate, SessionUpdate]):
    ...


session_crud = SessionCrud(Session)
