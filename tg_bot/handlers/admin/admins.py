from aiogram import Router, F
from aiogram.types import Message, BotCommand, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from models.admin_data import AdminData
from handlers.abstract_handler import AbstractHandler
from filters.chat_type import ChatTypeFilter
from filters.is_admin import IsAdmin
from src.template_engine import AbstractTemplateEngine
from states.add_admin_states import AddAdmin
from keyboards.inline.inline_keyboard_generator import InlineKeyboardGenerator

from services.admin_service import AdminService
from services.message_service import MessageService


class AdminAdminsHandler(AbstractHandler):
    def __init__(self, template_engine: AbstractTemplateEngine, admin_service: AdminService) -> None:
        self.__template_engine: AbstractTemplateEngine = template_engine
        self.__admin_service: AdminService = admin_service
        self.__message_service: MessageService = MessageService()
        self.__inline_keyboard_generator = InlineKeyboardGenerator()

        self.__router = Router()

    async def get_router(self) -> Router:
        await self.__register_handlers()
        return self.__router

    async def __register_handlers(self) -> None:
        self.__router.message.filter(ChatTypeFilter("private"), IsAdmin())

        self.__router.message.register(self.__get_admins, F.text == "Все админы")
        self.__router.message.register(self.__add_admin_by_id, F.text == "Добавить админа")
        self.__router.message.register(self.__add_admin, AddAdmin.admin_id)
        self.__router.message.register(self.__del_admin, F.text == "Удалить админа")
        self.__router.callback_query.register(self.__callback_del_admin, F.data.startswith("del_admin"))

    async def get_commands(self) -> list[BotCommand]:
        return []

    async def __get_admins(self, message: Message) -> None:
        admins: list[AdminData] = await self.__admin_service.get_admins()
        text: str = await self.__template_engine.render("admin/show_admins.tfb", data={"admins": admins})
        await message.answer(text)

    async def __add_admin_by_id(self, message: Message, state: FSMContext) -> None:
        text: str = await self.__template_engine.render("admin/enter_id.tfb")
        await message.answer(text)
        await state.set_state(AddAdmin.admin_id)

    async def __add_admin(self, message: Message, state: FSMContext) -> None:
        await state.clear()
        try:
            tg_id = int(str(message.text))
        except (ValueError, TypeError):
            text: str = await self.__template_engine.render("admin/invalid_id.tfb")
            await message.answer(text)
            return

        success: bool = await self.__admin_service.add_admin(tg_id)
        template_name: str = "admin/new_admin_success.tfb" if success else "admin/new_admin_failing.tfb"
        text = await self.__template_engine.render(template_name)
        await message.answer(text)

    async def __del_admin(self, message: Message) -> None:
        text: str = await self.__template_engine.render("admin/select_admin.tfb")
        admins: list[AdminData] = await self.__admin_service.get_admins()
        admins_id: dict[str, int] = {f"admin: {admin.tg_id}": admin.tg_id for admin in admins}
        markups: InlineKeyboardMarkup = await self.__inline_keyboard_generator.get_keyboard(admins_id, "del_admin")
        await message.answer(text, reply_markup=markups)

    async def __callback_del_admin(self, callback: CallbackQuery) -> None:
        try:
            admin_id = int(callback.data.split("_")[-1])  # type: ignore
        except (ValueError, IndexError):
            await callback.answer("Ошибка формата данных", show_alert=True)
            return

        success: bool = await self.__admin_service.delete_admin(admin_id)
        template_name: str = "admin/del_admin_success.tfb" if success else "admin/del_admin_failing.tfb"
        text: str = await self.__template_engine.render(template_name)

        await self.__message_service.edit_message(callback, text)
