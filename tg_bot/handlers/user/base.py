from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, BotCommand
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup

from handlers.abstract_handler import AbstractHandler
from filters.chat_type import ChatTypeFilter
from src.template_engine import AbstractTemplateEngine
from keyboards.default.user import UserNotLoggedMarkupsKeyboard


class BaseHandler(AbstractHandler):
    def __init__(self, template_engine: AbstractTemplateEngine) -> None:
        self.__template_engine: AbstractTemplateEngine = template_engine

        self.__not_logged_keyboard: ReplyKeyboardMarkup = UserNotLoggedMarkupsKeyboard().get_keyboard()

        self.__router: Router = Router()
        self.__router.message.filter(ChatTypeFilter("private"))

    async def get_router(self) -> Router:
        await self.__register_handlers()
        return self.__router

    async def __register_handlers(self) -> None:
        self.__router.message.register(self.__start, CommandStart())
        self.__router.message.register(self.__help, Command("help"))

    async def get_commands(self) -> list[BotCommand]:
        commands: list[BotCommand] = [
            BotCommand(command="start", description="перезапустить бота"),
            BotCommand(command="help", description="помощь"),
        ]
        return commands

    async def __start(self, message: Message) -> None:
        text: str = await self.__template_engine.render("start.tfb")
        await message.answer(text, reply_markup=self.__not_logged_keyboard)

    async def __help(self, message: Message) -> None:
        text: str = await self.__template_engine.render("help.tfb")
        await message.answer(text)
