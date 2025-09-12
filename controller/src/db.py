from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from models.db_models.admin import Base


class AbstractDb(ABC):
    @abstractmethod
    def __init__(self, db_config: dict) -> None:
        pass

    @abstractmethod
    async def get_session_factory(self) -> async_sessionmaker[AsyncSession]:
        pass

    @abstractmethod
    async def create_tables(self) -> None:
        pass


class Database(AbstractDb):
    def __init__(self, db_config: dict) -> None:
        self.engine: AsyncEngine = create_async_engine(
            f"postgresql+asyncpg://{db_config['user']}:{db_config['password']}"
            f"@{db_config['host']}:{db_config['port']}/{db_config['database']}",
            pool_size=20,
            max_overflow=10,
            pool_recycle=3600,
        )

        self.__session_factory: async_sessionmaker = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False
        )

    async def get_session_factory(self) -> async_sessionmaker:
        return self.__session_factory

    async def create_tables(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
