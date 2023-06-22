from typing import Literal
from pydantic import BaseModel


class LoginResponse(BaseModel):
    access_token: str
    token_type: Literal['bearer'] = 'bearer'
