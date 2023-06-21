from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


from src.core import Base, settings


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(settings.app.max_string_length), unique=True, index=True
    )
    password: Mapped[str] = mapped_column(String(1024))
    first_name: Mapped[str] = mapped_column(
        String(settings.app.max_string_length), nullable=True
    )
    last_name: Mapped[str] = mapped_column(
        String(settings.app.max_string_length), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
