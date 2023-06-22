from fastapi import APIRouter, Depends
from src.core.dependencies import session_manager
from src.managers.session import SessionManager

from src.schemas.session import SessionCreate, SessionDB


router = APIRouter(prefix='/session', tags=['Admin'])


@router.get(path='', response_model=list[SessionDB])
async def get_sessions(session_manager: SessionManager = Depends(session_manager)):
    return await session_manager.get_all()


@router.post(path='', response_model=SessionDB)
async def create_session(
    schema: SessionCreate, session_manager: SessionManager = Depends(session_manager)
):
    return await session_manager.create(schema)


@router.get(path='/{session_id}', response_model=SessionDB)
async def get_session(
    session_id: int, session_manager: SessionManager = Depends(session_manager)
):
    return await session_manager.get(id=session_id)


@router.delete(path='/{session_id}', response_model=SessionDB)
async def delete_session(
    session_id: int, session_manager: SessionManager = Depends(session_manager)
):
    session = await session_manager.get(id=session_id)
    return await session_manager.remove(session)


@router.patch(path='/{session_id}', response_model=SessionDB)
async def patch_session(
    session_id: int, session_manager: SessionManager = Depends(session_manager)
):
    session = await session_manager.get(id=session_id)
    return await session_manager.remove(session)
