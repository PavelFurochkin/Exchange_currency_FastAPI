from decimal import Decimal

from src.schemas.base import BaseSchema
from typing import Annotated
from pydantic import Field, PositiveInt, field_serializer

from src.schemas.currencies import CurrencySchema


class ExchangeSchemasIn(BaseSchema):
    """
    Класс для передачи данных в БД
    """
    id: PositiveInt
    base_currencies: Annotated[CurrencySchema, Field(..., description='Базовая валюта')]
    target_currencies: Annotated[CurrencySchema, Field(..., description='Целевая валюта')]
    rate: Annotated[Decimal, Field(..., max_length=9, min_length=6, gt=0)]


class ExchangeSchemasOut(BaseSchema):
    """
    Класс для корректного отображения полей в документации и округления до сотых
    """
    id: PositiveInt
    base_currencies: Annotated[CurrencySchema, Field(serialization_alias='baseCurrency')]
    target_currencies: Annotated[CurrencySchema, Field(serialization_alias='targetCurrency')]
    rate: Annotated[Decimal, Field(max_length=9, min_length=6, gt=0)]

    @field_serializer("rate")
    def format_rate(self, value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"))
