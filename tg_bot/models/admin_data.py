"""
Модуль с моделью данных админа.
"""

from pydantic import BaseModel


class AdminData(BaseModel):
    """Модель данных админа.

    :param tg_id: Уникальный идентификатор пользователя телеграмм
    """

    tg_id: int
