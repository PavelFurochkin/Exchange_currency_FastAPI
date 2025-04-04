from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.DAO.base_repository import BaseRepository
from src.models.currencies_model import Currency
from src.schemas.currency_schemas import CurrencySchema


class CurrencyRepository(BaseRepository[Currency, CurrencySchema]):
    def _get_model(self) -> type[Currency]:
        return Currency

    async def get_by_code(self, session: AsyncSession, code: str) -> Currency | None:
        """Получить валюту по коду."""
        stmt = select(self._get_model()).where(self._get_model().code == code)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

