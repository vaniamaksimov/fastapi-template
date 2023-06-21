from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from src.core.dependencies import user_manager

from src.managers.user import UserManager
from src.schemas.user import UserCreateAdmin, UserDB, UserUpdateAdmin


router = APIRouter(prefix='/user')


@router.get(path='', response_model=list[UserDB])
async def get_users(user_manager: UserManager = Depends(user_manager)):
    return await user_manager.get_all()


@router.post(path='', response_model=UserDB)
async def create_user(
    schema: UserCreateAdmin, user_manager: UserManager = Depends(user_manager)
):
    return await user_manager.create(schema)


@router.delete(path='/{user_id}', response_model=UserDB, deprecated=True)
async def delete_user(user_id: int):
    raise HTTPException(status_code=HTTPStatus.METHOD_NOT_ALLOWED)


@router.patch(path='/{user_id}', response_model=UserDB)
async def patch_user(
    user_id: int,
    schema: UserUpdateAdmin,
    user_manager: UserManager = Depends(user_manager),
):
    user = await user_manager.get(id=user_id)
    return await user_manager.update(user, schema)
