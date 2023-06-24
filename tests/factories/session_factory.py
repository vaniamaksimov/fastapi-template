import factory

from src.models.session import Session
from tests.factories.user_factory import UserFactory


class SessionFactory(factory.Factory):
    class Meta:
        model = Session

    user = factory.SubFactory(UserFactory)
