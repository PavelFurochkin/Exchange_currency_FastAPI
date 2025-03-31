from asyncpg import NumericValueOutOfRangeError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


from src.DAO.currency_repository import CurrencyRepository
from src.schemas.currency_schemas import CurrencySchema
from src.exceptions import exceptions


class CurrencyService:
    def __init__(self, repository: CurrencyRepository):
        self.repository = repository

    async def get_currency_by_code(
            self,
            session: AsyncSession,
            code: str
    ) -> CurrencySchema:
        """Получить валюту по коду с валидацией"""
        try:
            currency = await self.repository.get_by_code(session, code)
            return CurrencySchema.model_validate(currency, from_attributes=True)
        except ValidationError:
            raise exceptions.CurrencyAccessError(code)

    async def create_currency(
            self,
            session: AsyncSession,
            currency_data: CurrencySchema
    ) -> CurrencySchema:
        """Создать новую валюту"""
        try:
            created_currency = await self.repository.create(session, currency_data)
            return CurrencySchema.model_validate(created_currency, from_attributes=True)
        except NumericValueOutOfRangeError:
            raise exceptions.OutOfRangeError('Code ***, Name 3*-24*, Sign *')
        except IntegrityError:
            raise exceptions.AlreadyExistError()

    async def get_all_currency(self, session: AsyncSession) -> list[CurrencySchema]:
        currencies = await self.repository.get_all(session)
        return [CurrencySchema.model_validate(c, from_attributes=True) for c in currencies]

