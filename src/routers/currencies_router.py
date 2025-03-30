from fastapi import APIRouter, Depends, Form, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from src.database import get_db
from src.dependencies import get_currency_service
from src.schemas.currency_schemas import CurrencySchema
from src.service.currency_service import CurrencyService

router = APIRouter(tags=["currencies"])


@router.get("/currencies")
async def get_currencies(
        data: Annotated[CurrencyService, Depends(get_currency_service)],
        session: Annotated[AsyncSession, Depends(get_db)],
) -> list[CurrencySchema]:
    return await data.get_all_currency(session)


@router.post("/currencies")
async def post_currencies(
        data: Annotated[CurrencyService, Depends(get_currency_service)],
        currency: Annotated[CurrencySchema, Form()],
        session: Annotated[AsyncSession, Depends(get_db)],
) -> CurrencySchema:
    return await data.create_currency(session, currency)


@router.get("/currency/{code}")
async def get_currency(
        data: Annotated[CurrencyService, Depends(get_currency_service)],
        code: Annotated[str, Path(max_length=3, min_length=3, pattern="^[A-Z]{3}$")],
        session: Annotated[AsyncSession, Depends(get_db)],
) -> CurrencySchema:
    return await data.get_currency_by_code(session, code)
