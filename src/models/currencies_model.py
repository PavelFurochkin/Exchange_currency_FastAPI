from sqlalchemy import String

from src.models.base_model import Base

from sqlalchemy.orm import Mapped, mapped_column


class Currency(Base):
    """
    Модель SQLAlchemy для валюты
    """
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(3), index=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(24), index=True, unique=True, nullable=False)
    sign: Mapped[str] = mapped_column(String(3), nullable=False)

    def __repr__(self):
        return f'Currency: (id = {self.id}, code = {self.code}, name = {self.name}, sign = {self.sign}'

    def __str__(self):
        return f'{self.name} ({self.code})'
