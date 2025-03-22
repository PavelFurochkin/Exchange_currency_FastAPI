from decimal import Decimal

from fastapi import APIRouter, Depends, Form, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated, cast

from database import get_db
from dependencies import get_exchange_service
from schemas.exchange_rate_schemas import ExchangeSchemasOut, ExchangeSchemasCodeIn
from service.exchange_rate_service import ExchangeRateService

router = APIRouter(tags=["exchange_rates"])


@router.get("/exchange-rates")
async def get_exchange_rates(
        data: Annotated[ExchangeRateService, Depends(get_exchange_service)],
        session: Annotated[AsyncSession, Depends(get_db)],
) -> list[ExchangeSchemasOut]:
    return cast(list[ExchangeSchemasOut], data.get_all_rate(session))


@router.get("/exchange-rate/{codes}")
async def get_exchange_rate(
        data: Annotated[ExchangeRateService, Depends(get_exchange_service)],
        codes: Annotated[str, Path(title='The currency pair to get', min_length=6, max_length=6, example='USDEUR')],
        session: Annotated[AsyncSession, Depends(get_db)],
) -> ExchangeSchemasOut:
    base_code, target_code = codes[:3], codes[3:]
    return cast(ExchangeSchemasOut, data.get_rate(session, base_code, target_code))


@router.post("/exchange-rates/{codes}")
async def create_exchange_rates(
        data: Annotated[ExchangeRateService, Depends(get_exchange_service)],
        exchange_rate: Annotated[ExchangeSchemasCodeIn, Form()],
        session: Annotated[AsyncSession, Depends(get_db)],
) -> ExchangeSchemasOut:
    return cast(ExchangeSchemasOut, data.create_exchange_rate(session, exchange_rate))


@router.patch("/exchange-rate/{codes}")
async def update_exchange_rate(
        data: Annotated[ExchangeRateService, Depends(get_exchange_service)],
        codes: Annotated[str, Path(title='The currency pair to update', min_length=6, max_length=6, example='USDEUR')],
        rate: Annotated[Decimal, Query(gt=0), Form()],
        session: Annotated[AsyncSession, Depends(get_db)],
) -> ExchangeSchemasOut:
    base_code, target_code = codes[:3], codes[3:]
    return await data.update_exchange_rate(session, base_code, target_code, rate)
