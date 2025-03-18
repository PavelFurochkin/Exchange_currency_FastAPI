from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.controller import currencies_controller, exchange_controller, exchange_rates_controller
from src.middlewares import register_middlewares
from src.database import session_factory, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Функция lifespan, которая вызывается один раз при старте приложения и
    один раз при его завершении. Здесь мы инициализируем движок и фабрику сессий.
    """
    app.state.session_factory = session_factory
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


async def get_db(request: Request) -> AsyncSession:
    """
    Зависимость FastAPI, возвращающая асинхронную сессию.
    На каждый запрос создаём новую сессию через session_factory из app.state.
    """
    session_factory: async_sessionmaker[AsyncSession] = request.app.state.session_factory
    async with session_factory() as session:
        yield session


app.include_router(currencies_controller.router, prefix="/currencies")
app.include_router(exchange_controller.router, prefix="/exchange")
app.include_router(exchange_rates_controller.router, prefix="/exchange_rates")

register_middlewares(app)
