from pathlib import Path

from pydantic_settings import SettingsConfigDict, BaseSettings


class Setting(BaseSettings):
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent


app_setting = Setting()


class DBSettings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @property
    def database_url(self):
        return f'''postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'''

    model_config = SettingsConfigDict(
        env_file=app_setting.ROOT_DIR / ".env"
    )


db_settings = DBSettings()
