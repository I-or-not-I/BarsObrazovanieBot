from sqlalchemy.ext.asyncio import async_sessionmaker

from models.api_models.admin_data import AdminData
from routers.base import BaseRouter
from services.admin_service import AdminService


class Router(BaseRouter):
    def __init__(self, session_factory: async_sessionmaker, prefix: str = "/admin") -> None:
        self.__admin_service: AdminService = AdminService(session_factory)
        register_paths: tuple = (
            ("/get_admins", self.__get_admins, ["GET"]),
            ("/new_admin", self.__new_admin, ["POST"]),
            ("/del_admin", self.__del_admin, ["POST"]),
        )
        super().__init__(register_paths, prefix)

    async def __get_admins(self) -> list[AdminData]:
        return await self.__admin_service.get_admins()

    async def __new_admin(self, data: AdminData) -> bool:
        return await self.__admin_service.new_admin(data)

    async def __del_admin(self, data: AdminData) -> bool:
        return await self.__admin_service.del_admin(data)
