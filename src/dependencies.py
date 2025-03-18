from DAO.currency_repository import CurrencyRepository
from DAO.exchange_repository import ExchangeRepository
from service.currency_service import CurrencyService
from service.exchange_rate_service import ExchangeRateService


def get_currency_service():
    return CurrencyService(CurrencyRepository())


def get_exchange_service():
    return ExchangeRateService(
        currency_repo=CurrencyRepository(),
        exchange_repo=ExchangeRepository()
    )
