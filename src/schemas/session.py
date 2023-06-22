from datetime import datetime
from pydantic import BaseModel, Extra, IPvAnyAddress


class SessionBase(BaseModel):
    class Config:
        extra = Extra.forbid


class SessionCreate(SessionBase):
    ip: IPvAnyAddress | None
    user_id: int

    class Config(SessionBase.Config):
        ...


class SessionUpdate(SessionBase):
    ip: IPvAnyAddress | None

    class Config(SessionBase.Config):
        ...


class SessionDB(BaseModel):
    id: int
    created_at: datetime
    ip: IPvAnyAddress | None

    class Config:
        orm_mode = True
