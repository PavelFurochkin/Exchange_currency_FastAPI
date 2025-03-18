from decimal import Decimal

from src.schemas.base_scheme import BaseSchema
from typing import Annotated
from pydantic import Field, PositiveInt, field_serializer

from src.schemas.currency_schemas import CurrencySchema


class ExchangeSchemasIn(BaseSchema):
    """
    Класс для передачи данных в БД
    """
    id: PositiveInt
    base_currency_id: Annotated[int, Field(..., description='ID базовой валюты')]
    target_currency_id: Annotated[int, Field(..., description='ID целевой валюты')]
    rate: Annotated[Decimal, Field(..., max_digits=9, gt=0, decimal_places=6)]


class ExchangeSchemasOut(BaseSchema):
    """
    Класс для корректного отображения полей в документации и округления до сотых
    """
    id: PositiveInt
    base_currency: Annotated[CurrencySchema, Field(serialization_alias='baseCurrency')]
    target_currency: Annotated[CurrencySchema, Field(serialization_alias='targetCurrency')]
    rate: Annotated[Decimal, Field(max_digits=9, gt=0, decimal_places=6)]

    @field_serializer("rate")
    def format_rate(self, value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"))
