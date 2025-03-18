from fastapi import HTTPException, status
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
            return CurrencySchema.model_validate(currency)
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
            return CurrencySchema.model_validate(created_currency)
        except IntegrityError:
            raise exceptions.AlreadyExistError()

    async def get_all_currency(self, session: AsyncSession) -> list[CurrencySchema]:
        currencies = await self.repository.get_all(session)
        return [CurrencySchema.model_validate(c) for c in currencies]

