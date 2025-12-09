from typing import Callable, Optional, cast
from fastapi import APIRouter
from fastapi import APIRouter, HTTPException
from functools import wraps

from routers.abstract import AbstractRouter
from models.user_data import UserData
from src.parser import AbstractParser


def require_cookies(endpoint: Callable) -> Callable:
    @wraps(endpoint)
    async def wrapper(self, data: UserData, *args, **kwargs):
        if data.cookies is None:
            raise HTTPException(status_code=400, detail="Cookies are required")
        return await endpoint(self, data, *args, **kwargs)

    return wrapper


class DnevnikRouter(AbstractRouter):
    def __init__(self, parser: AbstractParser, prefix: str = "/dnevnik") -> None:
        self.__parser: AbstractParser = parser
        self.__router: APIRouter = APIRouter(prefix=prefix)

        self.__register_paths: dict = {
            "get_person_data": self.__get_person_data,
            "get_summary_marks": self.__get_summary_marks,
            "get_diary": self.__get_diary,
            "get_week_schedule": self.__get_week_schedule,
            "get_school_info": self.__get_school_info,
            "get_homework_from_range": self.__get_homework_from_range,
            "get_missed_lessons": self.__get_missed_lessons,
        }

        self.__routs_register()

    def __routs_register(self) -> None:
        for path, endpoint in self.__register_paths.items():
            self.__router.add_api_route(f"/{path}", endpoint, methods=["POST"], response_model=Optional[dict])

    async def __parser_call(self, parser_method: Callable, cookies: dict) -> dict:
        try:
            result = await parser_method(cookies)
            if result is None:
                raise HTTPException(404, "Data not found")
            return result
        except Exception as e:
            raise HTTPException(500, f"Parser error: {str(e)}")

    @require_cookies
    async def __get_person_data(self, data: UserData) -> dict | None:
        cookies = cast(dict, data.cookies)
        return await self.__parser_call(self.__parser.get_person_data, cookies)

    @require_cookies
    async def __get_summary_marks(self, data: UserData) -> dict | None:
        cookies = cast(dict, data.cookies)
        return await self.__parser_call(self.__parser.get_summary_marks, cookies)

    @require_cookies
    async def __get_diary(self, data: UserData) -> dict | None:
        cookies = cast(dict, data.cookies)
        return await self.__parser_call(self.__parser.get_diary, cookies)

    @require_cookies
    async def __get_week_schedule(self, data: UserData) -> dict | None:
        cookies = cast(dict, data.cookies)
        return await self.__parser_call(self.__parser.get_week_schedule, cookies)

    @require_cookies
    async def __get_school_info(self, data: UserData) -> dict | None:
        cookies = cast(dict, data.cookies)
        return await self.__parser_call(self.__parser.get_school_info, cookies)

    @require_cookies
    async def __get_homework_from_range(self, data: UserData) -> dict | None:
        cookies = cast(dict, data.cookies)
        return await self.__parser_call(self.__parser.get_homework_from_range, cookies)

    @require_cookies
    async def __get_missed_lessons(self, data: UserData) -> dict | None:
        cookies = cast(dict, data.cookies)
        return await self.__parser_call(self.__parser.get_missed_lessons, cookies)

    def get_router(self) -> APIRouter:
        return self.__router

    def get_endpoints(self) -> tuple:
        return tuple(self.__register_paths.keys())
