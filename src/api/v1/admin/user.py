from fastapi import APIRouter


router = APIRouter(prefix='/user')


@router.get(path='')
async def get_users():
    return 'user'
