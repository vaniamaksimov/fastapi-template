from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import wrapt

from src.utils.app_exceptions.crud import BaseCrudError


@wrapt.decorator
async def crud_error_handler(couroutine, instance, args, kwargs):
    try:
        return await couroutine(*args, **kwargs)
    except BaseCrudError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=e.message)


@wrapt.decorator
async def integrity_error_handler(couroutine, instance, args, kwargs):
    try:
        return await couroutine(*args, **kwargs)
    except IntegrityError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Не удалось выполнить запрос, оригинал ошибки: {e}',
        )
