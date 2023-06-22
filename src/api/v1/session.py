from fastapi import APIRouter

from src.schemas.session import SessionDB


router = APIRouter(prefix='/session', tags=['Session'])


@router.get(path='', response_model=list[SessionDB])
async def user_sessions():
    ...


@router.delete(path='/{session_id}', response_model=SessionDB)
async def delete_session(session_id: int):
    ...
