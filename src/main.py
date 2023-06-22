from fastapi import Depends, FastAPI
from src.api import router
from src.core.dependencies import add_current_user_to_request, add_db_session_to_request

app = FastAPI(
    dependencies=[
        Depends(add_db_session_to_request),
        Depends(add_current_user_to_request),
    ]
)
app.include_router(router)
