from decimal import Decimal

from fastapi import APIRouter, Path, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated, cast

from database import get_db
from dependencies import get_exchange_service
from schemas.exchange_schemas import ExchangeRateSchema, ExchangeRateSchemaIn
from service.exchange_rate_service import ExchangeRateService

router = APIRouter(tags=["exchange"])


@router.get("exchange")
async def get_exchange(
        data: Annotated[ExchangeRateService, Depends(get_exchange_service)],
        exchange: Annotated[ExchangeRateSchemaIn, Query()],
        session: Annotated[AsyncSession, Depends(get_db)],
) -> ExchangeRateSchema:
    return cast(
        ExchangeRateSchema,
        data.get_convert(session, exchange.amount, exchange.base_currency, exchange.target_currency)
    )
