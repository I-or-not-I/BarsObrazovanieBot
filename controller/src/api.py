import logging
import abc
from json import decoder
from typing import Any
import httpx
from pydantic import BaseModel


class AbstractApi(abc.ABC):
    @abc.abstractmethod
    def __init__(self, controller_ip: str, timeout: float) -> None:
        pass


class Api(AbstractApi):
    def __init__(self, controller_ip: str, timeout: float) -> None:
        self.__controller_ip: str = controller_ip.rstrip("/")
        self.__timeout: float = timeout

        self.__paths: dict = {}

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
