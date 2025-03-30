import asyncio
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from src.DAO.currency_repository import CurrencyRepository
from src.DAO.exchange_repository import ExchangeRepository
from src.exceptions.exceptions import DataBaseError
from src.schemas.currency_schemas import CurrencySchema
from src.schemas.exchange_rate_schemas import ExchangeSchemasCodeIn
from src.service.currency_service import CurrencyService
from src.service.exchange_rate_service import ExchangeRateService
from src.database import get_db

list_currencies = [
    {"name": "UnitedStatesDollar", "code": "USD", "sign": "$"},  # Доллар США
    {"name": "Euro", "code": "EUR", "sign": "€"},  # Евро
    {"name": "JapaneseYen", "code": "JPY", "sign": "¥"},  # Японская иена
    {"name": "BritishPound", "code": "GBP", "sign": "£"},  # Британский фунт стерлингов
    {"name": "SwissFranc", "code": "CHF", "sign": "Fr"},  # Швейцарский франк
]

exchange_rates = [
    {"base_currency_code": "USD", "target_currency_code": "EUR", "rate": 0.92},
    {"base_currency_code": "EUR", "target_currency_code": "USD", "rate": 1.09},
    {"base_currency_code": "USD", "target_currency_code": "JPY", "rate": 150.0},
    {"base_currency_code": "JPY", "target_currency_code": "USD", "rate": 0.0067},
    {"base_currency_code": "USD", "target_currency_code": "GBP", "rate": 0.79},
    {"base_currency_code": "GBP", "target_currency_code": "USD", "rate": 1.27},
    {"base_currency_code": "USD", "target_currency_code": "CHF", "rate": 0.88},
    {"base_currency_code": "CHF", "target_currency_code": "USD", "rate": 1.14},
]


async def seed_currencies(session: AsyncSession):
    currency_repo = CurrencyRepository()
    for currency_dict in list_currencies:
        await currency_repo.create(session, CurrencySchema(**currency_dict))


async def seed_exchange_rates(session: AsyncSession):
    exchange_repo = ExchangeRepository()
    for rate_dict in exchange_rates:
        await exchange_repo.create_exc_rate(
            session,
            base_code=rate_dict['base_currency_code'],
            target_code=rate_dict['target_currency_code'],
            rate=Decimal(rate_dict['rate'])
        )


async def main():
    async for session in get_db():
        await seed_currencies(session)
        await seed_exchange_rates(session)


if __name__ == '__main__':
    asyncio.run(main())
