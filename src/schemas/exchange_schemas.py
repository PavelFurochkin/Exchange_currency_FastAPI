from decimal import Decimal

from src.schemas.base_scheme import BaseSchema
from typing import Annotated
from pydantic import Field

from src.schemas.currency_schemas import CurrencySchema


class ExchangeRateSchema(BaseSchema):
    """
    Класс для передачи данных об обмене валюты пользователю
    """
    base_currency: Annotated[CurrencySchema, Field(..., serialization_alias='baseCurrency')]
    target_currency: Annotated[CurrencySchema, Field(..., serialization_alias='targetCurrency')]
    rate: Annotated[Decimal, Field(..., description='Обменный курс')]
    amount: Annotated[Decimal, Field(..., gt=0, decimal_places=2, description='Количество к обмену')]
    converted_amount: Annotated[Decimal, Field(decimal_places=2, serialization_alias='convertedAmount')]


class ExchangeRateSchemaIn(BaseSchema):
    """
    Класс для передачи данных об обмене валюты от пользователя
    """
    base_currency: Annotated[str, Field(..., serialization_alias='baseCurrency', min_length=3, max_length=3)]
    target_currency: Annotated[str, Field(..., serialization_alias='targetCurrency', min_length=3, max_length=3)]
    amount: Annotated[Decimal, Field(..., gt=0, decimal_places=2, description='Количество к обмену')]
