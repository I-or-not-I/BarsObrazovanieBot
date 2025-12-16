from typing import Any, Dict
from aiogram import Router, F
from aiogram.types import Message, BotCommand
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup

from handlers.abstract_handler import AbstractHandler
from src.template_engine import AbstractTemplateEngine
from states.login_states import LoginStates
from keyboards.default.user import UserNotLoggedMarkupsKeyboard, UserAllMarkupsKeyboard

from services.login_service import LoginService


class LoginHandler(AbstractHandler):
    def __init__(self, template_engine: AbstractTemplateEngine, login_service: LoginService) -> None:
        self.__template_engine: AbstractTemplateEngine = template_engine
        self.__login_service: LoginService = login_service

        self.__not_logged_keyboard: ReplyKeyboardMarkup = UserNotLoggedMarkupsKeyboard().get_keyboard()
        self.__logged_keyboard: ReplyKeyboardMarkup = UserAllMarkupsKeyboard().get_keyboard()

        self.__router = Router()

    async def get_router(self) -> Router:
        await self.__register_handlers()
        return self.__router

    async def __register_handlers(self) -> None:
        self.__router.message.register(self.__login, F.text == "Войти")
        self.__router.message.register(self.__process_login, LoginStates.waiting_for_login)
        self.__router.message.register(self.__process_password, LoginStates.waiting_for_password)
        self.__router.message.register(self.__process_sms_code, LoginStates.waiting_for_sms_code)

    async def get_commands(self) -> list[BotCommand]:
        return []

    async def __login(self, message: Message, state: FSMContext) -> None:
        await state.clear()
        text: str = await self.__template_engine.render("login/enter_login.tfb")
        ask_msg: Message = await message.answer(text)
        await state.update_data(ask_message_id=ask_msg.message_id)
        await state.set_state(LoginStates.waiting_for_login)

    async def __process_login(self, message: Message, state: FSMContext) -> None:
        await message.delete()
        data: Dict[str, Any] = await state.get_data()
        ask_message_id: Any | None = data.get("ask_message_id")
        if ask_message_id and message.bot:
            await message.bot.delete_message(message.chat.id, ask_message_id)

        login: str | None = message.text
        await state.update_data(login=login)

        text: str = await self.__template_engine.render("login/enter_password.tfb")
        ask_msg: Message = await message.answer(text)
        await state.update_data(ask_message_id=ask_msg.message_id)
        await state.set_state(LoginStates.waiting_for_password)

    async def __process_password(self, message: Message, state: FSMContext) -> None:
        await message.delete()

        data = await state.get_data()
        ask_message_id: Any | None = data.get("ask_message_id")
        if ask_message_id and message.bot:
            await message.bot.delete_message(message.chat.id, ask_message_id)

        password: str | None = message.text
        data: Dict[str, Any] = await state.get_data()
        login: str | None = data.get("login")

        if login is None or password is None:
            text: str = await self.__template_engine.render("login/incorrect_data.tfb")
            await message.answer(text)
            await state.clear()
            return

        wait_text: str = await self.__template_engine.render("login/wait.tfb")
        wait_msg: Message = await message.answer(wait_text)
        await self.__login_service.login(message.chat.id, login, password)
        if  message.bot:
            await message.bot.delete_message(message.chat.id, wait_msg.message_id)

        text: str = await self.__template_engine.render("login/enter_sms.tfb")
        ask_msg: Message = await message.answer(text)
        await state.update_data(ask_message_id=ask_msg.message_id)
        await state.set_state(LoginStates.waiting_for_sms_code)

    async def __process_sms_code(self, message: Message, state: FSMContext) -> None:
        await message.delete()

        data: Dict[str, Any] = await state.get_data()
        ask_message_id: Any | None = data.get("ask_message_id")
        if ask_message_id and message.bot:
            await message.bot.delete_message(message.chat.id, ask_message_id)

        sms_code: str | None = message.text
        if sms_code is None:
            text: str = await self.__template_engine.render("login/incorrect_data.tfb")
            await message.answer(text)
            return

        wait_text: str = await self.__template_engine.render("login/wait.tfb")
        wait_msg: Message = await message.answer(wait_text)
        ans: bool | None = await self.__login_service.sms_login(message.chat.id, sms_code)
        if  message.bot:
            await message.bot.delete_message(message.chat.id, wait_msg.message_id)

        if ans:
            text: str = await self.__template_engine.render("login/success.tfb")
            await message.answer(text, reply_markup=self.__logged_keyboard)
        else:
            text: str = await self.__template_engine.render("login/fail.tfb")
            await message.answer(text, reply_markup=self.__not_logged_keyboard)

        await state.clear()
