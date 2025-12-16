from models.admin_data import AdminData
from src.api import AdminApi


class AdminService:
    def __init__(self, api: AdminApi) -> None:
        self.__api: AdminApi = api

    async def get_admins(self) -> list[AdminData]:
        return await self.__api.get_admins()

    async def add_admin(self, tg_id: int) -> bool:
        user_data = AdminData(tg_id=tg_id)
        return await self.__api.new_admin(user_data)

    async def delete_admin(self, tg_id: int) -> bool:
        user_data = AdminData(tg_id=tg_id)
        return await self.__api.del_admin(user_data)
