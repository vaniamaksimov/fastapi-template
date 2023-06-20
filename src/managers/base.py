from typing import Generic

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.app_types import (
    CreateSchemaType,
    CrudType,
    ModelType,
    UpdateSchemaType,
)
from src.utils.decorators import crud_error_handler, integrity_error_handler


class BaseManager(Generic[ModelType, CrudType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        session: AsyncSession,
        request: Request | None = None,
        crud: CrudType = None,
    ) -> None:
        self.session = session
        self.request = request
        self.crud = crud

    async def _before_create(self, schema: CreateSchemaType) -> CreateSchemaType:
        return schema

    @integrity_error_handler
    async def create(self, schema: CreateSchemaType) -> ModelType:
        create_schema = await self._before_create(schema)
        db_obj = await self.crud.create(session=self.session, schema=create_schema)
        await self._after_create(db_obj)
        return db_obj

    async def _after_create(self, db_obj: ModelType) -> None:
        ...

    async def _before_get(self, **kwargs) -> None:
        ...

    @crud_error_handler
    async def get(self, **kwargs) -> ModelType:
        await self._before_get(**kwargs)
        db_obj = await self.crud.get(session=self.session, **kwargs)
        await self._after_create(db_obj)
        return await self.crud.get(self.session, **kwargs)

    async def _after_get(self, db_obj: ModelType) -> None:
        ...

    async def _before_get_all(self, **kwargs) -> None:
        ...

    @crud_error_handler
    async def get_all(self, **kwargs) -> list[ModelType]:
        await self._before_get_all(**kwargs)
        db_objs = await self.crud.get(self.session, **kwargs)
        await self._after_get_all(db_objs)
        return db_objs

    async def _after_get_all(self, db_objs: list[ModelType]) -> None:
        ...

    async def _before_update(
        self, db_obj: ModelType, schema: UpdateSchemaType
    ) -> UpdateSchemaType:
        return schema

    @integrity_error_handler
    async def update(self, db_obj: ModelType, schema: UpdateSchemaType) -> ModelType:
        update_schema = await self._before_update(db_obj, schema)
        db_obj = await self.crud.update(
            session=self.session, database_object=db_obj, schema=update_schema
        )
        await self._after_update(db_obj)
        return db_obj

    async def _after_update(self, db_obj: ModelType) -> None:
        ...

    async def _before_remove(self, db_obj: ModelType) -> None:
        ...

    @integrity_error_handler
    async def remove(self, db_obj: ModelType) -> ModelType:
        await self._before_remove(db_obj)
        db_obj = await self.crud.remove(session=self.session, database_object=db_obj)
        await self._after_remove(db_obj)
        return db_obj

    async def _after_remove(self, db_obj: ModelType) -> None:
        ...
