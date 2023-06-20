from passlib import pwd
from passlib.context import CryptContext
from src.core import settings


class PasswordHelper:
    def __init__(self, context: CryptContext = None) -> None:
        self.context = context or CryptContext(
            schemes=[settings.app.crypt_schema.get_secret_value()],
            deprecated='auto',
        )

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self.context.verify(
            secret=plain_password,
            hash=hashed_password,
        )

    def hash(self, password: str) -> str:
        return self.context.hash(password)

    def generate(self) -> str:
        return pwd.genword()


password_helper = PasswordHelper()
