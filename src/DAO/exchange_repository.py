from fastapi import HTTPException
from sqlalchemy import select, and_, DECIMAL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from DAO.abstract.base_repository import BaseRepository
from models.currencies_model import Currency
from models.exchange_rates_model import ExchangeRate
from schemas.exchange_rate_schemas import ExchangeSchemasIn


class ExchangeRepository(BaseRepository[ExchangeRate, ExchangeSchemasIn]):
    def _get_model(self) -> type[ExchangeRate]:
        return ExchangeRate

    async def get_by_currency_codes(
            self,
            session: AsyncSession,
            base_code: str,
            target_code: str,
            with_currencies: bool = True
    ) -> ExchangeRate | None:
        """
        Найти курс обмена по кодам валют.

        Args:
            base_code: Код базовой валюты (например, 'USD')
            target_code: Код целевой валюты (например, 'EUR')
            with_currencies: Загружать связанные объекты валют
        """
        stmt = select(self._get_model()).where(
            and_(
                self._get_model().base_currency.has(code=base_code),
                self._get_model().target_currency.has(code=target_code)
            )
        )

        if with_currencies:
            stmt = self._with_currencies(stmt)

        result = await session.execute(stmt)
        return result.scalars().first()

    async def update_rate_by_currencies_codes(
            self,
            session: AsyncSession,
            base_code: str,
            target_code: str,
            new_rate: DECIMAL,
            with_currencies: bool = True
    ) -> ExchangeRate:
        """
        Обновляет курс обмена по кодам валют.
        Возвращает обновленный курс с загруженными валютами.
        """
        try:
            rate = await self.get_by_currency_codes(
                session, base_code, target_code, with_currencies
            )
            if not rate:
                raise HTTPException(404, "Курс не найден")

            rate.rate = new_rate
            await session.commit()

            return rate
        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(500, "Ошибка обновления курса") from e

    def _with_currencies(self, stmt):
        """Добавляет загрузку связанных валют к запросу"""
        return stmt.options(
            joinedload(self._get_model().base_currency),
            joinedload(self._get_model().target_currency)
        )


