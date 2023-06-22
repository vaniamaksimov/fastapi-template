from fastapi import APIRouter
from .user import router as user_router
from .session import router as session_router

router = APIRouter(prefix='/admin')
router.include_router(user_router)
router.include_router(session_router)
