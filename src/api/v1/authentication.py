from fastapi import APIRouter


router = APIRouter(prefix='', tags=['Authentication'])


@router.post('/register')
async def register():
    ...


@router.post('/login')
async def login():
    ...


@router.get(path='/logout')
async def logout():
    ...
