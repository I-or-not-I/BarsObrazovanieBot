from typing import Any
from fastapi import APIRouter, HTTPException, status

from routers.abstract import AbstractRouter
from models.user_data import UserData
from src.login_parser import AbstractLoginParser


class LoginRouter(AbstractRouter):
    def __init__(self, parser: AbstractLoginParser, prefix: str = "/login") -> None:
        self.__parser: AbstractLoginParser = parser
        self.__router: APIRouter = APIRouter(prefix=prefix)

        self.__register_paths: dict = {
            "login": self.__login,
            "sms_login": self.__sms_login,
        }

        self.__routs_register()

    def __routs_register(self) -> None:
        for path, endpoint in self.__register_paths.items():
            self.__router.add_api_route(f"/{path}", endpoint, methods=["POST"])

    async def __login(self, data: UserData) -> bool:
        if not data.login or not data.password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login and password are required")

        try:
            result: bool = await self.__parser.login(data.login, data.password)
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials or user not found"
                )
            return result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Authentication failed: {str(e)}"
            ) from e

    async def __sms_login(self, data: UserData) -> dict[str, Any]:
        if not data.sms_code:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="SMS code is required")

        try:
            result = await self.__parser.sms_login(data.sms_code)
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid SMS code or session expired")
            return result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"SMS authentication failed: {str(e)}"
            ) from e

    def get_router(self) -> APIRouter:
        return self.__router

    def get_endpoints(self) -> tuple:
        return tuple(self.__register_paths.keys())
