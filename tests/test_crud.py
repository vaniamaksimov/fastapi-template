import pytest
import sqlparse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import user_crud
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from src.utils.app_exceptions.crud import InvalidAttrNameError, InvalidOperatorError
from tests.factories.user_factory import UserFactory


def parse(stmt):
    return sqlparse.format(str(stmt), reindent=True, keyword_case='upper')


async def test_crud_get(session: AsyncSession):
    users = UserFactory.build_batch(9)
    session.add_all(users)
    user = UserFactory(email='my-email@google.com')
    session.add(user)
    await session.commit()
    db_user = await user_crud.get(session, email='my-email@google.com')
    assert len(db_user) == 1
    assert db_user[0] == user


async def test_crud_create(session: AsyncSession, user_create_schema: UserCreate):
    user = await user_crud.create(session, user_create_schema)
    assert user
    db_obj = await session.execute(select(User))
    db_obj = db_obj.scalars().all()
    assert len(db_obj) == 1
    assert db_obj[0] == user


async def test_crud_delete(session: AsyncSession):
    user = UserFactory()
    session.add(user)
    await session.commit()
    db_user = await session.execute(select(User))
    db_user = db_user.scalars().all()
    db_customer = await session.execute(select(User))
    db_customer = db_customer.scalars().all()
    assert len(db_user) == 1
    assert db_user[0] == user
    assert len(db_customer) == 1
    assert db_customer[0].id == db_user[0].id
    del_obj = await user_crud.remove(session, user)
    assert user == del_obj
    db_user = await session.execute(select(User))
    db_user = db_user.scalars().all()
    db_customer = await session.execute(select(User))
    db_customer = db_customer.scalars().all()
    assert len(db_user) == 0
    assert len(db_customer) == 0


async def test_crud_update(session: AsyncSession, user_update_schema: UserUpdate):
    user = UserFactory(first_name='OldFirstName', last_name='OldLastName')
    session.add(user)
    await session.commit()
    db_user = (
        (await session.execute(select(User).where(User.first_name == user.first_name)))
        .scalars()
        .first()
    )
    assert db_user.first_name == user.first_name
    assert db_user.last_name == user.last_name
    updated_user = await user_crud.update(session, db_user, user_update_schema)
    assert db_user.id == updated_user.id
    assert updated_user.first_name == 'NewFirstName'
    assert updated_user.last_name == 'NewLastName'


@pytest.mark.parametrize(
    argnames=['kwargs', 'expected'],
    argvalues=[
        (None, select(User)),
        (
            {'email': 'email@gmail.com'},
            select(User).where(User.email == 'email@gmail.com'),
        ),
        (
            {'email__neq': 'email@gmail.com'},
            select(User).where(User.email != 'email@gmail.com'),
        ),
        (
            {'email__eq': 'email@gmail.com'},
            select(User).where(User.email == 'email@gmail.com'),
        ),
        (
            {'email': 'email@gmail.com', 'first_name': 'John'},
            select(User).where(
                (User.email == 'email@gmail.com') & (User.first_name == 'John')
            ),
        ),
    ],
)
def test_crud_make_statement(kwargs, expected):
    stmt = (
        user_crud._make_statement(**kwargs) if kwargs else user_crud._make_statement()
    )
    expected_stmt = expected
    assert parse(stmt) == parse(expected_stmt)


@pytest.mark.parametrize(
    argnames=['kwargs', 'exception'],
    argvalues=[
        ({'unexpected_field': 'some_value'}, InvalidAttrNameError),
        ({'unexpected_field__eq': 'some_value'}, InvalidAttrNameError),
        ({'email__unexpected_operator': 'some_value'}, InvalidOperatorError),
    ],
)
def test_crud_make_statement_raise_error(kwargs, exception):
    with pytest.raises(exception):
        user_crud._make_statement(**kwargs)
