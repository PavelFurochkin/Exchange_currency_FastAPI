from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from DAO.currency_repository import CurrencyRepository
from DAO.exchange_repository import ExchangeRepository
from schemas.currency_schemas import CurrencySchema
from schemas.exchange_rate_schemas import ExchangeSchemasOut, ExchangeSchemasIn


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
        await self._validate_currency_codes(session, base_code, target_code)

        # Прямой курс
        direct_rate = await self.exchange_repo.get_by_currency_codes(session, base_code, target_code)
        if direct_rate:
            return ExchangeSchemasOut.model_validate(direct_rate)

        # Обратный курс
        reverse_rate = await self.exchange_repo.get_by_currency_codes(session, target_code, base_code)
        if reverse_rate:
            return ExchangeSchemasOut(
                id=reverse_rate.id,
                base_currencies=reverse_rate.target_currency,
                target_currencies=reverse_rate.base_currency,
                rate=(Decimal(1)/reverse_rate.rate).quantize(Decimal(0.001))
            )

        # Конвертация через USD
        usd_rate = await self._get_rate_via_usd(session, base_code, target_code)
        if usd_rate:
            return ExchangeSchemasOut(
                id=0,
                base_currencies=CurrencySchema.model_validate(base_code),
                target_currencies=CurrencySchema.model_validate(target_code),
                rate=usd_rate,
            )

        raise HTTPException(404, "Курс не найден")

    async def _get_rate_via_usd(self, session: AsyncSession, base_code: str, target_code: str) -> Decimal | None:
        usd_code = 'USD'

        base_to_usd = await self._get_any_rate(session, base_code, usd_code)
        if not base_to_usd:
            return None

        usd_to_target = await self._get_any_rate(session, usd_code, target_code)
        if not usd_to_target:
            return None

        return (base_to_usd * usd_to_target).quantize(Decimal(0.000001))

    async def _get_any_rate(self, session: AsyncSession, base_code: str, target_code: str) -> Decimal | None:
        """Получает курс в любом направлении"""
        rate = await self.exchange_repo.get_by_currency_codes(session, base_code, target_code)
        if rate:
            return rate.rate

        reverse_rate = await self.exchange_repo.get_by_currency_codes(session, target_code, base_code)
        if reverse_rate:
            return Decimal(1) / reverse_rate.rate

        return None

    async def _validate_currency_codes(self, session: AsyncSession, *codes: str) -> None:
        for code in codes:
            if not await self.currency_repo.get_by_code(session, code):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Валюта {code} не найдена'
                )


