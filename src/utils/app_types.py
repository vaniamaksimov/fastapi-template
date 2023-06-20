from typing import TYPE_CHECKING, TypeVar

from pydantic import BaseModel

from src.core import Base

if TYPE_CHECKING:
    from src.crud.base import CrudBase

ModelType = TypeVar('ModelType', bound=Base)
CrudType = TypeVar("CrudType", bound="CrudBase")
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
