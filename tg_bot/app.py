"""
Основной модуль запуска телеграм-бота.
"""

import asyncio
from utils.logger import Logger
from filters.is_admin import IsAdmin
from models.admin_data import AdminData
from src.bot import AbstractTgBot, TgBot
from src.api import AbstractApi, Api
from src.template_engine import AbstractTemplateEngine, TemplateEngine
from config import CONTROLLER_IP, LOGGING_LEVEL, TIMEOUT, TEMPLATES_PATH, BOT_TOKEN


async def main() -> None:
    Logger(level=LOGGING_LEVEL)

    api: AbstractApi = Api(CONTROLLER_IP, TIMEOUT)
    await api.new_admin(AdminData(tg_id=1170348812)) 

    filter: IsAdmin = IsAdmin()
    for admin in await api.get_admins():
        await filter.add_admin(admin.tg_id)

    template_engine: AbstractTemplateEngine = TemplateEngine(TEMPLATES_PATH)

    bot: AbstractTgBot = TgBot(BOT_TOKEN, api, template_engine)

    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
