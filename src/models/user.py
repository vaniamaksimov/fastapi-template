from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
import enum


from src.core import Base, settings


@enum.unique
class Role(enum.StrEnum):
    CUSTOMER = 'CUSTOMER'
    ADMIN = 'ADMIN'


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(settings.app.max_string_length), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(1024))
    first_name: Mapped[str] = mapped_column(String(settings.app.max_string_length), nullable=True)
    last_name: Mapped[str] = mapped_column(String(settings.app.max_string_length), nullable=True)
    role: Mapped[Role] = mapped_column(Enum(Role, name='role'), default=Role.CUSTOMER)

    __mapper_args__ = {
        'polymorphic_on': role,
        'polymorphic_identity': None,
        'with_polymorphic': '*',
    }

    def __init__(self,
                 email: str,
                 password: str,
                 first_name: str | None = None,
                 last_name: str | None = None,
                 role: Role = Role.CUSTOMER):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.role = role


class Customer(User):
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', name='fk_customer_user_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        primary_key=True
    )

    __mapper_args__ = {
        'polymorphic_identity': Role.CUSTOMER
    }


class Admin(User):
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', name='fk_admin_user_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        primary_key=True
    )

    __mapper_args__ = {
        'polymorphic_identity': Role.ADMIN
    }
