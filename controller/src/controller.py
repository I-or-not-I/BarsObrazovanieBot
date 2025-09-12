"""
Модуль контроллера для обработки команд Telegram-бота.

Предоставляет:
- Абстрактный интерфейс для обработки команд
- Конкретную реализацию бизнес-логики бота
- Интеграцию с API, шаблонами сообщений и клавиатурами

Основные функции:
- Обработка команд /start и /help
- Управление данными пользователя (регистрация, обновление)
- Получение и отображение образовательных данных (оценки, расписание)
- Формирование ответов в формате Telegram API

Компоненты:
    AbstractController: Абстрактный интерфейс контроллера
    Controller: Конкретная реализация бизнес-логики

Зависимости:
    AbstractApi: Для взаимодействия с внешними сервисами
    AbstractTemplateEngine: Для генерации текста сообщений
    AbstractMarkups: Для создания клавиатурных разметок
    Pydantic-модели: Message, UserData, GetMarks, GetTimetable и др.

.. note::
    Все методы контроллера возвращают словари в формате,
    совместимом с Telegram Bot API.
"""

import abc
import logging

from src.api import AbstractApi
from src.db import AbstractDb


class AbstractController(abc.ABC):
    """
    Абстрактный базовый класс контроллера для обработки команд Telegram.

    :param api: Экземпляр API для взаимодействия с внешними сервисами
    :param template_engine: Движок шаблонов для генерации сообщений
    :param markups: Генератор клавиатурных разметок
    :type api: AbstractApi
    :type template_engine: AbstractTemplateEngine
    :type markups: AbstractMarkups
    """

    @abc.abstractmethod
    def __init__(self, api: AbstractApi, db: AbstractDb) -> None:
        """
        Абстрактный конструктор контроллера.

        :meta abstract:
        """


class Controller(AbstractController):
    """
    Конкретная реализация контроллера для обработки команд Telegram.

    :param api: Экземпляр API для взаимодействия с внешними сервисами
    :param template_engine: Движок шаблонов для генерации сообщений
    :param markups: Генератор клавиатурных разметок
    :type api: AbstractApi
    :type template_engine: AbstractTemplateEngine
    :type markups: AbstractMarkups
    :returns: Инициализированный экземпляр контроллера
    :rtype: Controller
    """

    def __init__(self, api: AbstractApi, db: AbstractDb) -> None:
        self.__api: AbstractApi = api
        self.__db: AbstractDb = db
