import logging
import abc
from json import decoder
from typing import Any
import httpx
from pydantic import BaseModel

from models.user_data import UserData
from models.admin_data import AdminData


class AbstractApi(abc.ABC):
    @abc.abstractmethod
    def __init__(self, controller_ip: str, timeout: float) -> None:
        pass


class BaseApi(AbstractApi):
    def __init__(self, api_ip: str, timeout: float) -> None:
        self.__api_ip: str = api_ip.rstrip("/")
        self.__timeout: float = timeout

    async def _get_data(self, path: str, data: BaseModel | None = None) -> Any | None:
        try:
            async with httpx.AsyncClient() as client:
                if data:
                    response: httpx.Response = await client.post(
                        f"{self.__api_ip}/{path}", json=data.model_dump(), timeout=self.__timeout
                    )
                else:
                    response: httpx.Response = await client.get(f"{self.__api_ip}/{path}", timeout=self.__timeout)
            response.raise_for_status()
        except (httpx.HTTPStatusError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.RequestError) as exc:
            logging.warning("Ошибка запроса к %s: %s", path, exc)
            return None
        try:
            return response.json()
        except decoder.JSONDecodeError:
            return None


class DnevnikApi(BaseApi):
    PATHS: dict = {
        "get_person_data": "dnevnik/get_person_data",
        "get_summary_marks": "dnevnik/get_summary_marks",
        "get_diary": "dnevnik/get_diary",
        "get_week_schedule": "dnevnik/get_week_schedule",
        "get_school_info": "dnevnik/get_school_info",
        "get_homework_from_range": "dnevnik/get_homework_from_range",
        "get_missed_lessons": "dnevnik/get_missed_lessons",
    }

    async def get_person_data(self, data: UserData) -> dict | None:
        path: str = self.PATHS["get_person_data"]
        return await self._get_data(path, data)

    async def get_summary_marks(self, data: UserData) -> dict | None:
        path: str = self.PATHS["get_summary_marks"]
        return await self._get_data(path, data)

    async def get_diary(self, data: UserData) -> dict | None:
        path: str = self.PATHS["get_diary"]
        return await self._get_data(path, data)

    async def get_week_schedule(self, data: UserData) -> dict | None:
        path: str = self.PATHS["get_week_schedule"]
        return await self._get_data(path, data)

    async def get_school_info(self, data: UserData) -> dict | None:
        path: str = self.PATHS["get_school_info"]
        return await self._get_data(path, data)

    async def get_homework_from_range(self, data: UserData) -> dict | None:
        path: str = self.PATHS["get_homework_from_range"]
        return await self._get_data(path, data)

    async def get_missed_lessons(self, data: UserData) -> dict | None:
        path: str = self.PATHS["get_missed_lessons"]
        return await self._get_data(path, data)


class LoginApi(BaseApi):
    PATHS: dict = {
        "login": "login/login",
        "sms_login": "login/sms_login",
    }

    async def login(self, data: UserData) -> bool | None:
        path: str = self.PATHS["login"]
        return await self._get_data(path, data)

    async def sms_login(self, data: UserData) -> bool | None:
        path: str = self.PATHS["sms_login"]
        return await self._get_data(path, data)


class AdminApi(BaseApi):
    PATHS: dict = {
        "get_admins": "admin/get_admins",
        "new_admin": "admin/new_admin",
        "del_admin": "admin/del_admin",
    }

    async def get_admins(self) -> list[AdminData]:
        admins: list | None = await self._get_data(self.PATHS["get_admins"])
        if admins is None:
            return []
        return [AdminData(**admin) for admin in admins]

    async def new_admin(self, user_data: AdminData) -> bool:
        validate: bool | None = await self._get_data(self.PATHS["new_admin"], user_data)
        if validate is None:
            validate = False
        return validate

    async def del_admin(self, user_data: AdminData) -> bool:
        validate: bool | None = await self._get_data(self.PATHS["del_admin"], user_data)
        if validate is None:
            validate = False
        return validate
