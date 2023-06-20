import pytest

from src.utils import password_helper


def test_password_helper_hash_password(password: str):
    hashed_password = password_helper.hash(password)
    assert hashed_password
    assert hashed_password != password


@pytest.mark.parametrize(
    argnames=['hash', 'expected_result'],
    argvalues=[
        ('$2b$12$p3TuD6sX/972B5D1jT7FZu3vjdQ8gOrWr5ZHaJHNAXF0nOFzNTrjW', True),
        ('$2b$12$p3TuD6sX/972B5D1jT7FZu3vjdQ8gOrWr5ZHaJHNAXF1nOFzNTrjW', False),
    ]
)
def test_password_helper_validate_password(password: str, hash: str, expected_result: bool):
    verify_result = password_helper.verify(password, hash)
    assert verify_result == expected_result


def test_password_helper_generate_password():
    password = password_helper.generate()
    assert password
    assert isinstance(password, str)
