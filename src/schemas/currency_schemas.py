from src.schemas.base_scheme import BaseSchema
from typing import Annotated
from pydantic import Field, PositiveInt


class CurrencySchema(BaseSchema):
    """
    Класс для передачи данных о валюте
    """
    id: PositiveInt | None = None
    code: Annotated[str, Field(min_length=3, max_length=3, description="Код валюты")]
    name: Annotated[str, Field(min_length=3, max_length=25, description="Полное имя валюты")]
    sign: Annotated[str, Field(min_length=1, max_length=3, description="Символ валюты")]
