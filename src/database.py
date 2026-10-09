from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine("sqlite+aiosqlite:///mydb.db", echo=True)
new_async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_async_session() as session:
        yield session

# Базовый класс для всех моделей SQLAlchemy.
class Base(DeclarativeBase):
    pass