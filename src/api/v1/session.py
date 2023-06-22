from fastapi import APIRouter, Depends, Request
from src.core.dependencies import only_authorized, session_manager
from src.managers.session import SessionManager

from src.schemas.session import SessionDB


router = APIRouter(
    prefix='/session', tags=['Session'], dependencies=[Depends(only_authorized)]
)


@router.get(path='', response_model=list[SessionDB])
async def user_sessions(request: Request):
    return await request.state.user.awaitable_attrs.sessions


@router.delete(path='/{session_id}', response_model=SessionDB)
async def delete_session(
    session_id: int, session_manager: SessionManager = Depends(session_manager)
):
    session = await session_manager.get(id=session_id)
    session
    return
