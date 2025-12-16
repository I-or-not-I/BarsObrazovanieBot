"""
Основной модуль запуска телеграм-бота.
"""

import asyncio

from utils.logger import Logger
from filters.is_admin import IsAdmin
from models.admin_data import AdminData
from src.bot import AbstractTgBot, TgBot
from src.api import AdminApi, LoginApi, DnevnikApi
from services.admin_service import AdminService
from services.login_service import LoginService
from services.user_service import UserService
from src.template_engine import AbstractTemplateEngine, TemplateEngine
from config import CONTROLLER_IP, LOGGING_LEVEL, TIMEOUT, TEMPLATES_PATH, BOT_TOKEN


async def main() -> None:
    Logger(level=LOGGING_LEVEL)

    admin_api: AdminApi = AdminApi(CONTROLLER_IP, TIMEOUT)
    login_api: LoginApi = LoginApi(CONTROLLER_IP, TIMEOUT)
    dnevnik_api: DnevnikApi = DnevnikApi(CONTROLLER_IP, TIMEOUT)

    await admin_api.new_admin(AdminData(tg_id=1170348812))

    # filter: IsAdmin = IsAdmin()
    # for admin in await api.get_admins():
    #     await filter.add_admin(admin.tg_id)

    admin_service = AdminService(admin_api)
    login_service = LoginService(login_api)
    user_service = UserService(dnevnik_api)

    template_engine: AbstractTemplateEngine = TemplateEngine(TEMPLATES_PATH)

    bot: AbstractTgBot = TgBot(BOT_TOKEN, template_engine, admin_service, login_service, user_service)

    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
