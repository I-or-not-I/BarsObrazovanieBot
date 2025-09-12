from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
import logging


class MessageService:
    @staticmethod
    async def edit_message(callback: CallbackQuery, text: str, reply_markup=None) -> None:
        try:
            if callback.message:
                await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")  # type: ignore
            else:
                await callback.answer(text, show_alert=True)
        except TelegramBadRequest as exc:
            logging.error("Failed to edit message: %s", exc)
            await callback.answer(text, show_alert=True)
