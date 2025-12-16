from models.user_data import UserData
from src.api import LoginApi


class LoginService:
    def __init__(self, api: LoginApi) -> None:
        self.__api: LoginApi = api

    async def login(self, tg_id: int, login: str, password: str) -> bool | None:
        data = UserData(id=tg_id, login=login, password=password)
        return await self.__api.login(data)

    async def sms_login(self, tg_id: int, sms_code: str) -> bool | None:
        data = UserData(id=tg_id, sms_code=sms_code)
        return await self.__api.sms_login(data)
