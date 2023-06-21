from unittest.mock import MagicMock

from fastapi import HTTPException


from sqlalchemy.exc import IntegrityError
import pytest
from src.utils.app_exceptions.crud import InvalidAttrNameError

from src.utils.decorators import integrity_error_handler, crud_error_handler


async def test_integrity_decorator_raise_http_exception():
    @integrity_error_handler
    async def integrity_raise():
        raise IntegrityError(MagicMock(), MagicMock(), MagicMock())

    with pytest.raises(HTTPException):
        await integrity_raise()


async def test_crud_decorator_raise_http_exception():
    @crud_error_handler
    async def crud_raise():
        raise InvalidAttrNameError(MagicMock(), MagicMock())

    with pytest.raises(HTTPException):
        await crud_raise()
