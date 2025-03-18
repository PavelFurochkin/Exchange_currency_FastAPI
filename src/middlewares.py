from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def register_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],  # Разрешенные домены
        allow_credentials=True,  # Разрешить куки и учетные данные
        allow_methods=['*'],  # Разрешенные HTTP-методы (например, GET, POST)
        allow_headers=['*']  # Разрешенные заголовки

    )