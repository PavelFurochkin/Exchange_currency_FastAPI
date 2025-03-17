from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from DAO.currency_repository import CurrencyRepository
from schemas.currency_schemas import CurrencySchema


class CurrencyService:
    def __init__(self, repository: CurrencyRepository):
        self.repository = repository

    async def get_currency_by_code(
            self,
            session: AsyncSession,
            code: str
    ) -> CurrencySchema:
        """Получить валюту по коду с валидацией"""
        currency = self.repository.get_by_code(session, code)
        if not currency:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Валюта с кодом {code} не найдена'
            )
        return CurrencySchema.model_validate(currency)

    async def create_currency(
            self,
            session: AsyncSession,
            currency_data: CurrencySchema
    ) -> CurrencySchema:
        """Создать новую валюту"""
        existing = await self.repository.get_by_code(session, currency_data.code)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'Валюта с таким кодом уже существую'
            )

        created_currency = await self.repository.create(session, currency_data)
        return CurrencySchema.model_validate(created_currency)


