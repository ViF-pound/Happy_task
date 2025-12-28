from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import config


url = f"postgresql+asyncpg://{config.env_data.POSTGRES_USER}:{config.env_data.POSTGRES_PASSWORD}@localhost:5432/{config.env_data.POSTGRES_DB}"

engine = create_async_engine(url = url, echo=True)

async_session = async_sessionmaker(engine, class_=AsyncSession)

async def get_session():
    async with async_session() as session:
        yield session

class Base(DeclarativeBase):
    ...