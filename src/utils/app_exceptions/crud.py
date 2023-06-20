from typing import Protocol
from src.utils.app_types import ModelType


class MessageMixin(Protocol):
    message: str


class BaseCrudError(MessageMixin, Exception):
    ...


class InvalidAttrNameError(BaseCrudError):
    def __init__(self, collumn_name: str, model: ModelType, *args: object) -> None:
        self.message = f'''
        Поле {collumn_name} недоступно для
        объекта {model.__class__.__name__}'''


class InvalidOperatorError(BaseCrudError):
    def __init__(self, operator: str, *args: object) -> None:
        self.message = f'Недопустимый оператор {operator}'
