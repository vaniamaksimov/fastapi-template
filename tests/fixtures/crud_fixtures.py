import pytest

from src.schemas.user import UserCreate


@pytest.fixture
def user_create_schema() -> UserCreate:
    return UserCreate(email='email@mail.com',
                      password='superstrongpassword')
