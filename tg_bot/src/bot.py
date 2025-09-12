import logging
import abc
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from services.admin_service import AdminService

from src.api import AbstractApi
from src.template_engine import AbstractTemplateEngine

from handlers.abstract_handler import AbstractHandler
from handlers.admin.admins import AdminAdminsHandler
from handlers.admin.base import AdminBaseHandler
from handlers.user.base import BaseHandler


class AbstractTgBot(abc.ABC):
    @abc.abstractmethod
    def __init__(self, token: str) -> None:
        """Инициализация абстрактного бота"""

    @abc.abstractmethod
    def run(self) -> None:
        """Основной метод для запуска бота"""


class TgBot(Bot, AbstractTgBot):
    def __init__(self, token: str, api: AbstractApi, template_engine: AbstractTemplateEngine) -> None:
        logging.debug("Инициализация бота")
        super().__init__(token)
        self.__dispatcher = Dispatcher()
        self.__api: AbstractApi = api
        self.__template_engine: AbstractTemplateEngine = template_engine

        self.__admin_service: AdminService = AdminService(self.__api)

    async def run(self) -> None:
        handlers: list[AbstractHandler] = [
            AdminBaseHandler(self.__template_engine),
            AdminAdminsHandler(self.__template_engine, self.__admin_service),
            BaseHandler(self.__template_engine),
        ]

        bot_commands: list[BotCommand] = []
        for handler in handlers:
            bot_commands.extend(await handler.get_commands())
            self.__dispatcher.include_router(await handler.get_router())

        await self.set_my_commands(bot_commands, BotCommandScopeDefault())
        await self.delete_webhook(drop_pending_updates=True)

        logging.info("Бот запущен")
        await self.__dispatcher.start_polling(self)

        logging.info("Бот остановлен")
        await self.__dispatcher.storage.close()
        await self.session.close()
