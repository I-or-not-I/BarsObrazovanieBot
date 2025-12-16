from models.user_data import UserData
from src.api import DnevnikApi


class UserService:
    def __init__(self, api: DnevnikApi) -> None:
        self.__api: DnevnikApi = api

    async def get_person_data(self, tg_id: int) -> dict | None:
        data = UserData(id=tg_id)
        return await self.__api.get_person_data(data)

    async def get_summary_marks(self, tg_id: int) -> dict | None:
        data = UserData(id=tg_id)
        return await self.__api.get_summary_marks(data)

    async def get_diary(self, tg_id: int) -> dict | None:
        data = UserData(id=tg_id)
        return await self.__api.get_diary(data)

    async def get_week_schedule(self, tg_id: int) -> dict | None:
        data = UserData(id=tg_id)
        return await self.__api.get_week_schedule(data)

    async def get_school_info(self, tg_id: int) -> dict | None:
        data = UserData(id=tg_id)
        return await self.__api.get_school_info(data)
