from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.core.dependencies import session_manager, user_manager, user_session
from src.managers.session import SessionManager
from src.managers.user import UserManager
from src.models.session import Session
from src.schemas.login_response import LoginResponse
from src.schemas.user import UserCreate, UserDB

router = APIRouter(prefix='', tags=['Authentication'])


@router.post('/register', response_model=UserDB)
async def register(
    schema: UserCreate, user_manager: UserManager = Depends(user_manager)
):
    return await user_manager.create(schema)


@router.post('/login', response_model=LoginResponse)
async def login(
    login_data: OAuth2PasswordRequestForm = Depends(),
    user_manager: UserManager = Depends(user_manager),
):
    return await user_manager.login(login_data)


@router.get(path='/logout')
async def logout(
    user_session: Session = Depends(user_session),
    session_manager: SessionManager = Depends(session_manager),
):
    return await session_manager.remove(user_session)
