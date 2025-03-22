from decimal import Decimal

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.DAO.currency_repository import CurrencyRepository
from src.DAO.exchange_repository import ExchangeRepository
from src.schemas.currency_schemas import CurrencySchema
from src.schemas.exchange_rate_schemas import ExchangeSchemasOut, ExchangeSchemasCodeIn
from src.schemas.exchange_schemas import ExchangeRateSchema
from src.exceptions import exceptions


class ExchangeRateService:
    def __init__(self, exchange_repo: ExchangeRepository, currency_repo: CurrencyRepository):
        self.exchange_repo = exchange_repo
        self.currency_repo = currency_repo

    async def get_rate(
            self,
            session: AsyncSession,
            base_code: str,
            target_code: str,
    ) -> ExchangeSchemasOut:
        base_currency = await self._validate_currency_code(session, base_code)
        target_currency = await self._validate_currency_code(session, target_code)

        # Прямой курс
        direct_rate = await self.exchange_repo.get_by_currency_codes(session, base_code, target_code)
        if direct_rate:
            return ExchangeSchemasOut.model_validate(direct_rate)

        # Обратный курс
        reverse_rate = await self.exchange_repo.get_by_currency_codes(session, target_code, base_code)
        if reverse_rate:
            return ExchangeSchemasOut(
                id=reverse_rate.id,
                base_currency=reverse_rate.target_currency,
                target_currency=reverse_rate.base_currency,
                rate=(Decimal(1) / reverse_rate.rate).quantize(Decimal(0.001))
            )

        # Конвертация через USD
        usd_rate = await self._get_rate_via_usd(session, base_code, target_code)
        if usd_rate:
            return ExchangeSchemasOut(
                id=0,
                base_currency=CurrencySchema.model_validate(base_currency),
                target_currency=CurrencySchema.model_validate(target_currency),
                rate=usd_rate,
            )

        raise HTTPException(404, "Курс не найден")

    async def _get_rate_via_usd(self, session: AsyncSession, base_code: str, target_code: str) -> Decimal | None:
        usd_code = 'USD'

        base_to_usd = await self.exchange_repo.get_by_currency_codes(session, base_code, usd_code)
        if not base_to_usd:
            return None

        usd_to_target = await self.exchange_repo.get_by_currency_codes(session, usd_code, target_code)
        if not usd_to_target:
            return None

        return (base_to_usd.rate * usd_to_target.rate).quantize(Decimal(0.000001))

    async def _validate_currency_code(self, session: AsyncSession, code: str) -> CurrencySchema:
        try:
            currency = await self.currency_repo.get_by_code(session, code)
            return CurrencySchema.model_validate(currency)
        except ValidationError:
            raise exceptions.CurrencyAccessError(code)

    async def get_convert(
            self,
            session: AsyncSession,
            amount: Decimal,
            base_code: str,
            target_code: str
    ) -> ExchangeRateSchema:
        try:
            base_currency = await self._validate_currency_code(session, base_code)
            target_currency = await self._validate_currency_code(session, target_code)
            rate = await self.get_rate(session, base_code, target_code)
            amount_converted = rate.rate * amount
            return ExchangeRateSchema(
                base_currency=base_currency,
                target_currency=target_currency,
                rate=rate.rate,
                amount=amount,
                converted_amount=amount_converted
            )
        except ValidationError:
            raise exceptions.ExchangeRateNotExistError(base_code, target_code)

    async def get_all_rate(self, session: AsyncSession) -> list[ExchangeSchemasOut]:
        rates = await self.exchange_repo.get_all(session)
        return [ExchangeSchemasOut.model_validate(rate) for rate in rates]

    async def create_exchange_rate(
            self,
            session: AsyncSession,
            exchange_rate: ExchangeSchemasCodeIn
    ) -> ExchangeSchemasOut:
        try:
            create_exchange_rate = await self.exchange_repo.create(session, exchange_rate)
            return ExchangeSchemasOut.model_validate(create_exchange_rate)
        except IntegrityError:
            raise exceptions.AlreadyExistError()

    async def update_exchange_rate(
            self,
            session: AsyncSession,
            base_code: str,
            target_code: str,
            new_rate: Decimal,
    ) -> ExchangeSchemasOut:
        new_exchange_rate = await self.exchange_repo.update_rate_by_currencies_codes(
            session,
            base_code,
            target_code,
            new_rate
        )
        return ExchangeSchemasOut.model_validate(new_exchange_rate)
