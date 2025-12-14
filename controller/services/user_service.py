from typing import Tuple
import logging
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import Result, select
from sqlalchemy.exc import SQLAlchemyError

from services.abstract_service import AbstractService
from models.api_models.user_data import UserData
from models.db_models.user import User


class UserService(AbstractService):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.__session_factory: async_sessionmaker[AsyncSession] = session_factory

    async def new_user(self, data: UserData) -> bool:
        async with self.__session_factory() as session:
            try:
                result: Result[Tuple[User]] = await session.execute(select(User).where(User.id == data.id))
                user: User | None = result.scalar_one_or_none()
                if user is None:
                    new_user = User(id=data.id, cookies=data.cookies)
                    session.add(new_user)
                    await session.commit()
                    return True
                return False
            except SQLAlchemyError as e:
                await session.rollback()
                logging.error("Database error occurred while adding user: %s", e)
                return False

    async def change_user_cookies(self, data: UserData) -> bool:
        if data.cookies is None:
            logging.error("A database error occurred while modifying user cookies. Cookies were not received.")
            return False

        async with self.__session_factory() as session:
            try:
                result: Result[Tuple[User]] = await session.execute(select(User).where(User.id == data.id))
                user: User | None = result.scalar_one_or_none()
                if user is None:
                    return False
                user.cookies = data.cookies
                await session.commit()
                await session.refresh(user)
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                logging.error("Database error occurred while change user cookies: %s", e)
                return False

    async def get_user_cookies(self, data: UserData) -> dict | None:
        async with self.__session_factory() as session:
            try:
                result: Result[Tuple[User]] = await session.execute(select(User).where(User.id == data.id))
                user: User | None = result.scalar_one_or_none()
                if user is None:
                    return 
                return user.cookies
            except SQLAlchemyError as e:
                await session.rollback()
                logging.error("Database error occurred while change user cookies: %s", e)

    async def user_exist(self, data: UserData) -> bool:
        async with self.__session_factory() as session:
            try:
                result: Result[Tuple[User]] = await session.execute(select(User).where(User.id == data.id))
                user: User | None = result.scalar_one_or_none()
                if user is None:
                    return False
                return True
            except SQLAlchemyError as e:
                logging.error("Database error occurred while change user cookies: %s", e)
                return False