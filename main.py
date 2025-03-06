from fastapi import FastAPI
from src.controller import currencies_controller, exchange_controller, exchange_rates_controller


app = FastAPI()

app.include_router(currencies_controller.router, prefix="/currencies")
app.include_router(exchange_controller.router, prefix="/exchange")
app.include_router(exchange_rates_controller.router, prefix="/exchange_rates")


