from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """
    Класс с базовыми настройками для всех моделей
    """
    model_config = ConfigDict(
        from_attributes=True,  # Позволяет использовать для заполнения полей SQLAlchemy
        extra="ignore",  # Поля не входящие в модель игнорируются
        str_strip_whitespace=True,  # Удаляет пробелы в начале и в конце для str
    )
