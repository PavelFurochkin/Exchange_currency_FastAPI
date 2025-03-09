from src.schemas.base import BaseSchema
from typing import Annotated
from pydantic import Field, PositiveInt


class CurrencySchema(BaseSchema):
    """
    Класс для передачи данных о валюте
    """
    id: PositiveInt
    code: Annotated[str, Field(gt=2, lt=4, description="Код валюты")]
    name: Annotated[str, Field(gt=2, lt=25, description="Полное имя валюты")]
    sign: Annotated[str, Field(gt=0, lt=4, description="Символ валюты")]

