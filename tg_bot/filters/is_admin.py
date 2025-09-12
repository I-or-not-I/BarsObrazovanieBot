from typing import Self, Optional
from aiogram.types import Message
from aiogram.filters import Filter


class IsAdmin(Filter):
    _instance: Optional[Self] = None
    __admins: list[int] = []

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def __call__(self, message: Message) -> bool:
        return message.chat.id in self.__admins

    async def add_admin(self, admin_id: int) -> None:
        if admin_id not in self.__admins:
            self.__admins.append(admin_id)

    async def del_admin(self, admin_id: int) -> None:
        if admin_id in self.__admins:
            self.__admins.remove(admin_id)
