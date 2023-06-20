from passlib.pwd import genword
import factory

from src.models.user import Admin, Customer, Role, User


class UserFactory(factory.Factory):
    class Meta:
        model = User
        abstract = True

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(
        lambda user: f'{user.first_name}{user.last_name}@example.com'.lower()
    )
    password = factory.LazyAttribute(lambda _: genword())


class CustomerFactory(UserFactory):
    class Meta:
        model = Customer

    role = Role.CUSTOMER


class AdminFactory(UserFactory):
    class Meta:
        model = Admin

    role = Role.ADMIN
