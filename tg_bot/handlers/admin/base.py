from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, BotCommand
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup

from handlers.abstract_handler import AbstractHandler
from filters.chat_type import ChatTypeFilter
from filters.is_admin import IsAdmin
from src.template_engine import AbstractTemplateEngine
from keyboards.default.admin import AdminAllMarkupsKeyboard


class AdminBaseHandler(AbstractHandler):
    def __init__(self, template_engine: AbstractTemplateEngine) -> None:
        self.__template_engine: AbstractTemplateEngine = template_engine

        self.__keyboard: ReplyKeyboardMarkup = AdminAllMarkupsKeyboard().get_keyboard()

        self.__router: Router = Router()

    async def get_router(self) -> Router:
        await self.__register_handlers()
        return self.__router

    async def __register_handlers(self) -> None:
        self.__router.message.filter(ChatTypeFilter("private"), IsAdmin())

        self.__router.message.register(self.__start, CommandStart())
        self.__router.message.register(self.__help, Command("help"))

    async def get_commands(self) -> list[BotCommand]:
        commands: list[BotCommand] = [
            BotCommand(command="start", description="перезапустить бота"),
            BotCommand(command="help", description="помощь"),
        ]
        return commands

    async def __start(self, message: Message) -> None:
        text: str = await self.__template_engine.render("admin/start.tfb")
        await message.answer(text, reply_markup=self.__keyboard)

    async def __help(self, message: Message) -> None:
        text: str = await self.__template_engine.render("admin/help.tfb")
        await message.answer(text)
