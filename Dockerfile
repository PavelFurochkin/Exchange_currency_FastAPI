# Используем официальный образ Python
FROM python:3.11-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

# Устанавливаем системные зависимости (например, для компиляции и работы с PostgreSQL)
RUN apk update && apk add --no-cache gcc musl-dev postgresql-dev

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости через pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . .

# Команда для запуска FastAPI приложения (порт 8000)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]