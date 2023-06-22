from fastapi import APIRouter, Request


from .admin import router as admin_router
from .authentication import router as authentication_router
from .user import router as user_router
from .session import router as session_router
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/v1')
router.include_router(admin_router)
router.include_router(authentication_router)
router.include_router(user_router)
router.include_router(session_router)


@router.get(path='')
async def request_test(request: Request):
    db: AsyncSession = request.state.db_session
    print(db)
    # return await db.execute(select(User))
