from src.DAO.currency_repository import CurrencyRepository
from src.DAO.exchange_repository import ExchangeRepository
from src.service.currency_service import CurrencyService
from src.service.exchange_rate_service import ExchangeRateService


def get_currency_service():
    return CurrencyService(CurrencyRepository())


def get_exchange_service():
    return ExchangeRateService(
        currency_repo=CurrencyRepository(),
        exchange_repo=ExchangeRepository()
    )
