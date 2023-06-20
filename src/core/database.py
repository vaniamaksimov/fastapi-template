from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from .settings import settings


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


engine = create_async_engine(url=settings.db.url)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession)
