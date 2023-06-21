import pytest

from src.managers.user import UserManager


@pytest.fixture
def user_manager(session):
    return UserManager(session)
