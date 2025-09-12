"""
Модуль моделей данных пользователей.

Модели основаны на SQLAlchemy.
"""

from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from models.db_models.base import Base


class Admin(Base):

    __tablename__ = "admins"

    tg_id: Mapped[Integer] = mapped_column("tg_id", Integer, primary_key=True)

    def to_dict(self) -> dict:
        """Преобразует объект User в словарь для сериализации в JSON.

        :return: Словарь с основными атрибутами пользователя
        :rtype: dict

        .. warning::
            При изменении состава полей модели необходимо обновлять этот метод
        """
        return {
            "tg_id": self.tg_id,
        }
