import uvicorn
from fastapi import FastAPI

from src.routers import currencies_router, exchange_router, exchange_rates_router

from src.exceptions.handlers import register_exception_handlers
from src.middlewares import register_middlewares

app = FastAPI()

app.include_router(currencies_router.router)
app.include_router(exchange_router.router)
app.include_router(exchange_rates_router.router)

register_middlewares(app)
register_exception_handlers(app)


