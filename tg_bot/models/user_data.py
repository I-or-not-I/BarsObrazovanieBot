from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class UserData(BaseModel):

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, str_strip_whitespace=True)

    id: int = Field(
        alias="id",
        description="Уникальный числовой идентификатор пользователя в системе",
    )

    password: Optional[str] = Field(
        default=None,
        alias="password",
        description="Пароль от дневника",
    )

    login: Optional[str] = Field(
        default=None,
        alias="login",
        description="Логин от дневника",
    )

    sms_code: Optional[str] = Field(
        default=None,
        alias="sms_code",
        description="Код подтверждения",
    )

    cookies: Optional[dict] = Field(
        default=None,
        alias="cookies",
        description="Данные сессии в JSON-формате",
    )
