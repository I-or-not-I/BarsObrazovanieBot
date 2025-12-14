from typing import Any
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import async_sessionmaker

from routers.base import BaseRouter
from models.api_models.user_data import UserData
from services.user_service import UserService
from src.api import LoginApi
from services.user_service import User


class LoginRouter(BaseRouter):
    def __init__(self, parser: LoginApi, session_factory: async_sessionmaker, prefix: str = "/login") -> None:
        self.__parser: LoginApi = parser
        self.__user_service: UserService = UserService(session_factory)

        register_paths: tuple = (
            ("/login", self.__login, ["POST"]),
            ("/sms_login", self.__sms_login, ["POST"]),
        )
        super().__init__(register_paths, prefix)

    async def __login(self, data: UserData) -> bool | None:
        if not data.login or not data.password:
            raise HTTPException(status_code=401, detail="login, password are required")
        return await self.__parser.login(data)

    async def __sms_login(self, data: UserData) -> bool | None:
        if not data.sms_code:
            raise HTTPException(status_code=401, detail="sms code are required")
        cookies: dict | None = await self.__parser.sms_login(data)
        data.cookies = cookies
        if await self.__user_service.user_exist(data):
            return await self.__user_service.change_user_cookies(data)
        else:
            return await self.__user_service.new_user(data)
