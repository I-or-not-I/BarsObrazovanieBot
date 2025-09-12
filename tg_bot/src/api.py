import logging
import abc
from json import decoder
from typing import Any
import httpx
from pydantic import BaseModel

from models.admin_data import AdminData


class AbstractApi(abc.ABC):
    @abc.abstractmethod
    def __init__(self, controller_ip: str, timeout: float) -> None:
        """
        Абстрактный инициализатор API.

        :meta abstract:
        """

    @abc.abstractmethod
    async def get_admins(self) -> list[AdminData]:
        pass

    @abc.abstractmethod
    async def new_admin(self, user_data: AdminData) -> bool:
        pass

    @abc.abstractmethod
    async def del_admin(self, user_data: AdminData) -> bool:
        pass


class Api(AbstractApi):
    """
    Реализация API для взаимодействия с парсером через HTTP.

    :param controller_ip: IP-адрес или URL сервиса парсера
    :param timeout: Таймаут запросов в секундах
    :type controller_ip: str
    :type timeout: float
    :returns: Инициализированный экземпляр API
    :rtype: Api
    """

    def __init__(self, controller_ip: str, timeout: float) -> None:
        self.__controller_ip: str = controller_ip.rstrip("/")
        self.__timeout: float = timeout

        self.__paths: dict = {
            "get_admins": "get_admins",
            "new_admin": "new_admin",
            "del_admin": "del_admin",
        }

    async def __get_data(self, path: str, data: BaseModel | None = None) -> Any | None:
        try:
            async with httpx.AsyncClient() as client:
                if data:
                    response: httpx.Response = await client.post(
                        f"{self.__controller_ip}/{path}", json=data.model_dump(), timeout=self.__timeout
                    )
                else:
                    response: httpx.Response = await client.post(
                        f"{self.__controller_ip}/{path}", timeout=self.__timeout
                    )
            response.raise_for_status()
        except (httpx.HTTPStatusError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.RequestError) as exc:
            logging.warning("Ошибка запроса к %s: %s", path, exc)
            return None

        try:
            return response.json()
        except decoder.JSONDecodeError:
            return None

    async def get_admins(self) -> list[AdminData]:
        admins: list | None = await self.__get_data(self.__paths["get_admins"])
        if admins is None:
            return []
        return [AdminData(**admin) for admin in admins]

    async def new_admin(self, user_data: AdminData) -> bool:
        validate: bool | None = await self.__get_data(self.__paths["new_admin"], user_data)
        if validate is None:
            validate = False
        return validate

    async def del_admin(self, user_data: AdminData) -> bool:
        validate: bool | None = await self.__get_data(self.__paths["del_admin"], user_data)
        if validate is None:
            validate = False
        return validate
