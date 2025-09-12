from typing import Tuple
import logging
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import Result, select
from sqlalchemy.exc import SQLAlchemyError

from services.abstract_service import AbstractService
from models.api_models.admin_data import AdminData
from models.db_models.admin import Admin


class AdminService(AbstractService):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.__session_factory: async_sessionmaker[AsyncSession] = session_factory

    async def get_admins(self) -> list[AdminData]:
        async with self.__session_factory() as session:
            try:
                result: Result[Tuple[Admin]] = await session.execute(select(Admin))
                return [AdminData(**user.to_dict()) for user in result.scalars().all()]
            except SQLAlchemyError as e:
                logging.error("Database error occurred while fetching cards: %s", e)
                return []

    async def new_admin(self, data: AdminData) -> bool:
        async with self.__session_factory() as session:
            try:
                result: Result[Tuple[Admin]] = await session.execute(select(Admin).where(Admin.tg_id == data.tg_id))
                admin: Admin | None = result.scalar_one_or_none()
                if admin is None:
                    new_admin = Admin(tg_id=data.tg_id)
                    session.add(new_admin)
                    await session.commit()
                    return True
                return False
            except SQLAlchemyError as e:
                await session.rollback()
                logging.error("Database error occurred while adding admin: %s", e)
                return False

    async def del_admin(self, data: AdminData) -> bool:
        async with self.__session_factory() as session:
            try:
                result: Result[Tuple[Admin]] = await session.execute(select(Admin).where(Admin.tg_id == data.tg_id))
                admin: Admin | None = result.scalar_one_or_none()
                if admin is None:
                    return False
                await session.delete(admin)
                await session.commit()
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                logging.error("Database error occurred while deleting admin: %s", e)
                return False
