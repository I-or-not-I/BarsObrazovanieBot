from typing import Optional, Callable, cast
from functools import wraps
from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker

from routers.base import BaseRouter
from models.api_models.user_data import UserData
from src.api import DnevnikApi
from services.user_service import UserService


def require_cookies(endpoint: Callable) -> Callable:
    @wraps(endpoint)
    async def wrapper(self, data: UserData, *args, **kwargs):
        cookies = await self._user_service.get_user_cookies(data)
        if not cookies:
            raise HTTPException(status_code=401, detail="Cookies are required")
        data.cookies = cookies
        return await endpoint(self, data, *args, **kwargs)

    return wrapper


class DnevnikRouter(BaseRouter):
    def __init__(self, parser: DnevnikApi, session_factory: async_sessionmaker, prefix: str = "/dnevnik") -> None:
        self.__parser: DnevnikApi = parser
        self._user_service: UserService = UserService(session_factory)

        register_paths: tuple = (
            ("/get_person_data", self.__get_person_data, ["POST"]),
            ("/get_summary_marks", self.__get_summary_marks, ["POST"]),
            ("/get_diary", self.__get_diary, ["POST"]),
            ("/get_week_schedule", self.__get_week_schedule, ["POST"]),
            ("/get_school_info", self.__get_school_info, ["POST"]),
            ("/get_homework_from_range", self.__get_homework_from_range, ["POST"]),
            ("/get_missed_lessons", self.__get_missed_lessons, ["POST"]),
        )

        super().__init__(register_paths, prefix)

    @require_cookies
    async def __get_person_data(self, data: UserData) -> dict | None:
        return await self.__parser.get_person_data(data)

    @require_cookies
    async def __get_summary_marks(self, data: UserData) -> dict | None:
        return await self.__parser.get_summary_marks(data)

    @require_cookies
    async def __get_diary(self, data: UserData) -> dict | None:
        return await self.__parser.get_diary(data)

    @require_cookies
    async def __get_week_schedule(self, data: UserData) -> dict | None:
        return await self.__parser.get_week_schedule(data)

    @require_cookies
    async def __get_school_info(self, data: UserData) -> dict | None:
        return await self.__parser.get_school_info(data)

    @require_cookies
    async def __get_homework_from_range(self, data: UserData) -> dict | None:
        return await self.__parser.get_homework_from_range(data)

    @require_cookies
    async def __get_missed_lessons(self, data: UserData) -> dict | None:
        return await self.__parser.get_missed_lessons(data)
