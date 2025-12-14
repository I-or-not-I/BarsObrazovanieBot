from sqlalchemy import JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from models.db_models.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[Integer] = mapped_column(
        Integer,
        primary_key=True,
        doc="Уникальный числовой идентификатор пользователя в системе",
    )

    cookies: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        doc="Данные сессии в JSON-формате",
    )
