from sqlalchemy import ForeignKey, DECIMAL, UniqueConstraint

from src.models.base_model import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.currencies_model import Currency


class ExchangeRate(Base):
    """
    Модель SQLAlchemy для обменного курса
    """
    __tablename__ = 'exchange_rate'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    base_currency_id: Mapped[int] = mapped_column(
        ForeignKey("currency.id", ondelete="CASCADE"),
        nullable=False
    )
    target_currency_id: Mapped[int] = mapped_column(
        ForeignKey("currency.id", ondelete="CASCADE"),
        nullable=False
    )
    rate: Mapped[DECIMAL] = mapped_column(DECIMAL(precision=9, scale=6))

    base_currency: Mapped["Currency"] = relationship(foreign_keys='ExchangeRate.base_currency_id')
    target_currency: Mapped["Currency"] = relationship(foreign_keys='ExchangeRate.target_currency_id')

    __table_args__ = (
        UniqueConstraint('base_currency_id', 'target_currency_id', name='unique_currency_rate')
    )

    def __repr__(self):
        return f'Exchange pair: base = {self.base_currency_id} - target = {self.target_currency_id} rate = {self.rate}'
