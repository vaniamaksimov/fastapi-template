from pydantic import BaseModel


class TokenData(BaseModel):
    sid: int
