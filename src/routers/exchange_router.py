from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from src.database import get_db
from src.dependencies import get_exchange_service
from src.schemas.exchange_schemas import ExchangeRateSchema
from src.service.exchange_rate_service import ExchangeRateService

router = APIRouter(tags=["exchange"])


@router.get("/exchange")
async def get_exchange(
        data: Annotated[ExchangeRateService, Depends(get_exchange_service)],
        session: Annotated[AsyncSession, Depends(get_db)],
        base_currency: Annotated[str, Query(alias="from")] = None,
        target_currency: Annotated[str, Query(alias="to")] = None,
        amount: Annotated[Decimal | None, Query(ge=0)] = None,
        ) -> ExchangeRateSchema:
    return await data.get_convert(session, amount, base_currency, target_currency)
