class CurrencyExchangeError(Exception):
    """Базовый класс для обработки ошибок"""

    def __init__(self, *args):
        self.message = ''

    def __str__(self):
        return self.message


class DataBaseError(CurrencyExchangeError):
    """База данных недоступна"""
    def __init__(self, error, *args):
        self.message = f'Ошибка доступа к базе данных {error}'


class OutOfRangeError(CurrencyExchangeError):
    """Число не входит в допуск"""
    def __init__(self, format,  *args):
        self.message = f'Введеное значение не соответствует формату {format}'


class CurrencyAccessError(CurrencyExchangeError):
    """Валюта недоступна"""
    def __init__(self, code, *args):
        self.message = f'Возникла ошибка при обращении к валюте {code}'


class AlreadyExistError(CurrencyExchangeError):
    """Ошибка дублирования"""
    def __init__(self,  *args):
        self.message = f'Такая запись уже существует в базе данных'


class CurrencyExchangeError(CurrencyExchangeError):
    """Ошибка дублирования обменного курса"""
    def __init__(self,  *args):
        self.message = f'Такой обменный курс уже существует в базе данных'


class ExchangeRateNotExistError(CurrencyExchangeError):
    """Ошибка при конвертации"""
    def __init__(self, base_code, target_code,  *args):
        self.message = f'Произошла ошибка при рассчете обменного курса'