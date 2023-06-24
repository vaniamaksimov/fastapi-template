from fastapi import APIRouter, Depends

from src.core.dependencies import current_superuser, only_authorized

from .session import router as session_router
from .user import router as user_router

router = APIRouter(
    prefix='/admin', dependencies=[Depends(only_authorized), Depends(current_superuser)]
)
router.include_router(user_router)
router.include_router(session_router)
