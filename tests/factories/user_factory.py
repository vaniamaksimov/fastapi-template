from passlib.pwd import genword
import factory

from src.models.user import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(
        lambda user: f'{user.first_name}{user.last_name}@example.com'.lower()
    )
    password = factory.LazyAttribute(lambda _: genword())


class AdminFactory(UserFactory):
    is_superuser = True
