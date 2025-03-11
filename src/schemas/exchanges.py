from decimal import Decimal

from src.schemas.base import BaseSchema
from typing import Annotated
from pydantic import Field

from src.schemas.currencies import CurrencySchema


class ExchangeRateSchema(BaseSchema):
    """
    Класс для передачи данных об обмене валюты 
    """
    base_currency: Annotated[CurrencySchema, Field(..., serialization_alias='baseCurrency')]
    target_currency: Annotated[CurrencySchema, Field(..., serialization_alias='targetCurrency')]
    rate: Annotated[Decimal, Field(..., description='Обменный курс')]
    amount: Annotated[Decimal, Field(..., gt=0, decimal_places=2, description='Количество к обмену')]
    converted_amount: Annotated[Decimal, Field(decimal_places=2, serialization_alias='convertedAmount')]
