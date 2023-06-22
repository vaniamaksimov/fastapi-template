from http import HTTPStatus
from fastapi import HTTPException
from jose import JWTError, jwt

from src.core import settings
from src.schemas.token import TokenData
from pydantic import ValidationError


class TokenHelper:
    def __init__(self) -> None:
        self.secret = settings.app.secret_key.get_secret_value()
        self.algorithm = settings.app.algorithm.get_secret_value()

    def create(self, data: TokenData) -> str:
        return jwt.encode(data.dict(), self.secret, self.algorithm)

    def decode(self, token: str) -> TokenData:
        try:
            return TokenData(**jwt.decode(token, self.secret, [self.algorithm]))
        except (JWTError, ValidationError):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail='bad credentials'
            )


bearer_token_helper = TokenHelper()
