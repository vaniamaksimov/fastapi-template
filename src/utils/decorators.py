from functools import wraps
from http import HTTPStatus
from typing import Any, Coroutine

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.utils.app_exceptions.crud import BaseCrudError
from src.utils.app_types import ModelType


def crud_error_handler(coroutine: Coroutine[Any, Any, ModelType]):
    @wraps(coroutine)
    async def wrapper(*args, **kwargs):
        try:
            result = await coroutine(*args, **kwargs)
        except BaseCrudError as e:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=e.message)
        return result

    return wrapper


def integrity_error_handler(coroutine: Coroutine[Any, Any, ModelType]):
    @wraps(coroutine)
    async def wrapper(*args, **kwargs):
        try:
            result = await coroutine(*args, **kwargs)
        except IntegrityError as e:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'Не удалось выполнить запрос, оригинал ошибки: {e}',
            )
        return result

    return wrapper
