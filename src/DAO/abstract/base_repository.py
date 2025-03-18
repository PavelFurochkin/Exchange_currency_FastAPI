from abc import ABC, abstractmethod
from typing import Generic, TypeVar, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Select
from sqlalchemy.exc import NoResultFound

T = TypeVar('T')  # Тип модели SQLAlchemy
S = TypeVar('S')  # Тип Pydantic схемы


class BaseRepository(ABC, Generic[T, S]):
    @abstractmethod
    def _get_model(self) -> type[T]:
        """Возвращает класс модели SQLAlchemy."""
        pass

    async def get_by_id(self, session: AsyncSession, id: int) -> T | None:
        """Получить объект по ID"""
        stmt = select(self._get_model()).where(self._get_model().id == id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, session: AsyncSession) -> list[T]:
        """Получить все объекты."""
        stmt = select(self._get_model())
        result = await session.execute(stmt)
        return cast(list[T], result.scalars().all())

    async def create(self, session: AsyncSession, data: S) -> T:
        """Создать новый объект."""
        obj = self._get_model()(**data.model_dump())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def delete(self, session: AsyncSession, id: int) -> None:
        """Удалить объект."""
        obj = await self.get_by_id(session, id)
        if not obj:
            raise NoResultFound(f'{self._get_model().__name__} c id = {id} не найден')
        await session.delete(obj)
        await session.commit()
