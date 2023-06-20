from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from .base import CrudBase

class UserCrud(CrudBase[User, UserCreate, UserUpdate]): ...


user_crud = UserCrud(User)
