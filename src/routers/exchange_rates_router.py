from decimal import Decimal

from fastapi import APIRouter, Depends, Form, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated, cast

from src.database import get_db
from src.dependencies import get_exchange_service
from src.schemas.exchange_rate_schemas import ExchangeSchemasOut, ExchangeSchemasCodeIn
from src.service.exchange_rate_service import ExchangeRateService

router = APIRouter(tags=["exchange_rates"])


@router.get("/exchangeRates")
async def get_exchange_rates(
        data: Annotated[ExchangeRateService, Depends(get_exchange_service)],
        session: Annotated[AsyncSession, Depends(get_db)],
) -> list[ExchangeSchemasOut]:
    return  await data.get_all_rate(session)


@router.get("/exchangeRate/{codes}")
async def get_exchange_rate(
        data: Annotated[ExchangeRateService, Depends(get_exchange_service)],
        codes: Annotated[str, Path(title='The currency pair to get', min_length=6, max_length=6, example='USDEUR')],
        session: Annotated[AsyncSession, Depends(get_db)],
) -> ExchangeSchemasOut:
    base_code, target_code = codes[:3], codes[3:]
    return await data.get_rate(session, base_code, target_code)


@router.post("/exchangeRates")
async def create_exchange_rates(
        data: Annotated[ExchangeRateService, Depends(get_exchange_service)],
        session: Annotated[AsyncSession, Depends(get_db)],
        baseCurrencyCode: Annotated[str, Form()] = "",
        targetCurrencyCode: Annotated[str, Form()] = "",
        rate: Annotated[Decimal | None, Form(ge=0)] = None,
) -> ExchangeSchemasOut:
    return await data.create_exchange_rate(session, baseCurrencyCode, targetCurrencyCode, rate)


@router.patch("/exchangeRate/{codes}")
async def update_exchange_rate(
        data: Annotated[ExchangeRateService, Depends(get_exchange_service)],
        codes: Annotated[str, Path(title='The currency pair to update', min_length=6, max_length=6, example='USDEUR')],
        rate: Annotated[Decimal, Query(gt=0), Form()],
        session: Annotated[AsyncSession, Depends(get_db)],
) -> ExchangeSchemasOut:
    base_code, target_code = codes[:3], codes[3:]
    return await data.update_exchange_rate(session, base_code, target_code, rate)
