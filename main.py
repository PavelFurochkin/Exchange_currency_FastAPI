from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.routers import currencies_router, exchange_router, exchange_rates_router

from exceptions.handlers import register_exception_handlers
from src.middlewares import register_middlewares

app = FastAPI()


async def get_db(request: Request) -> AsyncSession:
    """
    Зависимость FastAPI, возвращающая асинхронную сессию.
    На каждый запрос создаём новую сессию через session_factory из app.state.
    """
    session_factory: async_sessionmaker[AsyncSession] = request.app.state.session_factory
    async with session_factory() as session:
        yield session


app.include_router(currencies_router.router, prefix="/currencies")
app.include_router(exchange_router.router, prefix="/exchange")
app.include_router(exchange_rates_router.router, prefix="/exchange_rates")

register_middlewares(app)
register_exception_handlers(app)
