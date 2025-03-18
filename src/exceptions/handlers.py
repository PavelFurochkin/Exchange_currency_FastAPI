from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from src.exceptions import exceptions


def register_exception_handlers(app: "FastAPI"):
    app.exception_handlers(exceptions.DataBaseError)

    async def database_error(request: Request, exc: exceptions.DataBaseError):
        return JSONResponse(
            status_code=500,
            content={"message": str(exc)}
        )

    app.exception_handlers(exceptions.CurrencyAccessError)

    async def currency_access(request: Request, exc: exceptions.CurrencyAccessError):
        return JSONResponse(
            status_code=404,
            content={"message": str(exc)}
        )

    app.exception_handlers(exceptions.AlreadyExistError)

    async def already_exist(request: Request, exc: exceptions.AlreadyExistError):
        return JSONResponse(
            status_code=409,
            content={"message": str(exc)}
        )

    app.exception_handlers(exceptions.CurrencyExchangeError)

    async def currency_exchange(request: Request, exc: exceptions.CurrencyExchangeError):
        return JSONResponse(
            status_code=404,
            content={"message": str(exc)}
        )

    app.exception_handlers(exceptions.ExchangeRateNotExistError)

    async def currencies_not_exist(request: Request, exc: exceptions.ExchangeRateNotExistError):
        return JSONResponse(
            status_code=404,
            content={"message": str(exc)}
        )
