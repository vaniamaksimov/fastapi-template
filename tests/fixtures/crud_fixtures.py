import pytest

from src.schemas.user import UserCreate, UserUpdate


@pytest.fixture
def user_create_schema() -> UserCreate:
    return UserCreate(email='email@mail.com', password='superstrongpassword')


@pytest.fixture
def user_update_schema() -> UserUpdate:
    return UserUpdate(first_name='NewFirstName', last_name='NewLastName')
