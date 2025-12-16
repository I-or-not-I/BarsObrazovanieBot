from aiogram import Router, F
from aiogram.types import Message, BotCommand

from handlers.abstract_handler import AbstractHandler
from src.template_engine import AbstractTemplateEngine

from services.user_service import UserService


class DnevnikHandler(AbstractHandler):
    def __init__(self, template_engine: AbstractTemplateEngine, user_service: UserService) -> None:
        self.__template_engine: AbstractTemplateEngine = template_engine
        self.__user_service: UserService = user_service

        self.__router = Router()

    async def get_router(self) -> Router:
        await self.__register_handlers()
        return self.__router

    async def __register_handlers(self) -> None:
        self.__router.message.register(self.__get_person_data, F.text == "Личные данные")
        self.__router.message.register(self.__get_summary_marks, F.text == "Сводка оценок")
        self.__router.message.register(self.__get_week_schedule, F.text == "Расписание на неделю")
        self.__router.message.register(self.__get_school_info, F.text == "Информация о школе")

    async def get_commands(self) -> list[BotCommand]:
        return []

    async def __get_person_data(self, message: Message) -> None:
        data: dict | None = await self.__user_service.get_person_data(message.chat.id)
        if data is None:
            return
        text: str = await self.__template_engine.render("user/person_data.tfb", data=data)
        await message.answer(text, parse_mode="html")

    async def __get_summary_marks(self, message: Message) -> None:
        data: dict | None = await self.__user_service.get_summary_marks(message.chat.id)
        if data is None:
            return
        text: str = await self.__template_engine.render("user/summary_marks.tfb", data=data)
        await message.answer(text, parse_mode="html")

    async def __get_week_schedule(self, message: Message) -> None:
        data: dict | None = await self.__user_service.get_week_schedule(message.chat.id)
        if data is None:
            return
        for day in data["days"]:
            text: str = await self.__template_engine.render("user/week_schedule.tfb", data=day)
            await message.answer(text, parse_mode="html")


    async def __get_school_info(self, message: Message) -> None:
        data: dict | None = await self.__user_service.get_school_info(message.chat.id)
        if data is None:
            return
        text: str = await self.__template_engine.render("user/school_info.tfb", data=data)
        await message.answer(text, parse_mode="html")
