from decimal import Decimal

from sqlalchemy import select, and_, insert, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from exceptions.exceptions import ExchangeRateNotExistError, DataBaseError
from src.DAO.abstract.base_repository import BaseRepository
from src.models.exchange_rates_model import ExchangeRate
from src.schemas.base_scheme import BaseSchema
from src.schemas.exchange_rate_schemas import ExchangeSchemasCodeIn


class ExchangeRepository(BaseRepository[ExchangeRate, BaseSchema]):
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
            session: Актуальная сессия
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
            new_rate: Decimal,
            with_currencies: bool = True
    ) -> ExchangeRate:
        """
        Обновляет курс обмена по кодам валют.
        Возвращает обновленный курс с загруженными валютами.
        """
        try:
            exc_rate = (
                update(self._get_model())
                .where(
                    self._get_model().base_currency.has(code=base_code),
                    self._get_model().target_currency.has(code=target_code)
                )
                .values(rate=new_rate)
                .returning(self._get_model())
            )

            result = await session.execute(exc_rate)
            updated_exc_rate = result.scalars().first()
            if not updated_exc_rate:
                raise ExchangeRateNotExistError(base_code, target_code)

            await session.commit()
            return updated_exc_rate
        except SQLAlchemyError as e:
            await session.rollback()
            raise DataBaseError(e)

    def _with_currencies(self, stmt):
        """Добавляет загрузку связанных валют к запросу"""
        return stmt.options(
            joinedload(self._get_model().base_currency),
            joinedload(self._get_model().target_currency)
        )

    async def create(self, session: AsyncSession, data: ExchangeSchemasCodeIn) -> ExchangeRate:
        base_currency = await self.get_by_code(session, data.base_currency_code)
        target_currency = await self.get_by_code(session, data.target_currency_code)
        new_exchange_rate = insert(self._get_model()).values(
            base_currency_id=base_currency.id,
            target_currency_id=target_currency.id,
            rate=data.rate
        ).returning(self._get_model())
        res = await session.execute(new_exchange_rate)
        await session.commit()
        await session.refresh(res)
        return res.scalars().first()
