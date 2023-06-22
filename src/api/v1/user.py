from fastapi import APIRouter

from src.schemas.user import UserDB


router = APIRouter(prefix='/user', tags=['User'])


@router.get(path='', response_model=UserDB)
async def current_user():
    ...


@router.patch(path='', response_model=UserDB)
async def patch_current_user():
    ...
