from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import db_settings

engine = create_async_engine(db_settings.database_url)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

