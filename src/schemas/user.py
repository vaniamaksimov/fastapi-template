from pydantic import BaseModel, EmailStr, Extra, Field

from src.core import settings


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        extra = Extra.forbid


class UserCreateAdmin(UserCreate):
    is_admin: bool

    class Config(UserCreate.Config):
        ...


class UserUpdate(BaseModel):
    first_name: str | None = Field(None, max_length=settings.app.max_string_length)
    last_name: str | None = Field(None, max_length=settings.app.max_string_length)

    class Config:
        extra = Extra.forbid


class UserUpdateAdmin(UserUpdate):
    is_admin: bool | None

    class Config(UserUpdate.Config):
        ...


class UserDB(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None
    last_name: str | None
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True
