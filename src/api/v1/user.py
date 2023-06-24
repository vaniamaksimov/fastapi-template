from fastapi import APIRouter, Depends, Request

from src.core.dependencies import only_authorized, user_manager
from src.managers.user import UserManager
from src.schemas.user import UserDB, UserUpdate

router = APIRouter(
    prefix='/user', tags=['User'], dependencies=[Depends(only_authorized)]
)


@router.get(path='', response_model=UserDB)
async def current_user(request: Request):
    return request.state.user


@router.patch(path='', response_model=UserDB)
async def patch_current_user(
    request: Request,
    schema: UserUpdate,
    user_manager: UserManager = Depends(user_manager),
):
    return await user_manager.update(request.state.user, schema)
