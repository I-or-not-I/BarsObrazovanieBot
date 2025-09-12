import abc
from sqlalchemy.ext.asyncio import async_sessionmaker


class AbstractService(abc.ABC):
    def __init__(self, session_factory: async_sessionmaker) -> None:
        pass
