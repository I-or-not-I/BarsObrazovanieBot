import abc
import logging
import httpx
from datetime import datetime

logger: logging.Logger = logging.getLogger(__name__)


class AbstractParser(abc.ABC):
    def __init__(self) -> None:
        pass

    async def get_person_data(self, cookies: dict) -> dict | None:
        pass

    async def get_summary_marks(self, cookies: dict) -> dict | None:
        pass

    async def get_diary(self, cookies: dict) -> dict | None:
        pass

    async def get_week_schedule(self, cookies: dict) -> dict | None:
        pass

    async def get_school_info(self, cookies: dict) -> dict | None:
        pass

    async def get_homework_from_range(self, cookies: dict) -> dict | None:
        pass

    async def get_missed_lessons(self, cookies: dict) -> dict | None:
        pass


class Parser(AbstractParser):
    def __init__(self, timeout: float) -> None:
        self.__timeout: float = timeout

    async def __request(self, url: str, cookies: dict, data: dict | None = None) -> httpx.Response | None:
        try:
            async with httpx.AsyncClient(verify=False) as client:
                if data:
                    response: httpx.Response = await client.post(
                        url, cookies=cookies, timeout=self.__timeout, data=data
                    )
                else:
                    response: httpx.Response = await client.get(url, cookies=cookies, timeout=self.__timeout)
            response.raise_for_status()
            return response
        except httpx.ReadTimeout as exc:
            logger.warning("Сервер долго не отвечает")
            return None
        except httpx.HTTPStatusError as exc:
            logger.warning("Ошибка парсинга: %s", exc)
            return None
        except Exception as exc:
            logger.error("Неизвестная ошибка %s", exc)
        return None

    async def get_person_data(self, cookies: dict) -> dict | None:
        url: str = "https://sh-open.ris61edu.ru/api/ProfileService/GetPersonData"
        response: httpx.Response | None = await self.__request(url, cookies)
        if response is None:
            logger.warning("Ошибка парсинга личных данных пользователя")
            return None
        return response.json()

    async def get_summary_marks(self, cookies: dict) -> dict | None:
        url: str = f"https://sh-open.ris61edu.ru/api/MarkService/GetSummaryMarks?date={datetime.today().date()}"
        response: httpx.Response | None = await self.__request(url, cookies)
        if response is None:
            logger.warning("Ошибка парсинга суммарных оценок пользователя")
            return None
        return response.json()

    async def get_diary(self, cookies: dict) -> dict | None:
        data = {"date": f"{datetime.today().date()}", "is_diary": False}
        url: str = "https://sh-open.ris61edu.ru/api/ScheduleService/GetDiary"
        response: httpx.Response | None = await self.__request(url, cookies, data)
        if response is None:
            logger.warning("Ошибка парсинга дневника")
            return None
        return response.json()

    async def get_week_schedule(self, cookies: dict) -> dict | None:
        url: str = f"https://sh-open.ris61edu.ru/api/ScheduleService/GetWeekSchedule?date={datetime.today().date()}"
        response: httpx.Response | None = await self.__request(url, cookies)
        if response is None:
            logger.warning("Ошибка парсинга недельного расписания")
            return None
        return response.json()

    async def get_school_info(self, cookies: dict) -> dict | None:
        url: str = "https://sh-open.ris61edu.ru/api/SchoolService/getSchoolInfo"
        response: httpx.Response | None = await self.__request(url, cookies)
        if response is None:
            logger.warning("Ошибка парсинга школьной информации")
            return None
        return response.json()

    async def get_homework_from_range(self, cookies: dict) -> dict | None:
        url: str = "https://sh-open.ris61edu.ru/api/HomeworkService/GetHomeworkFromRange"
        response: httpx.Response | None = await self.__request(url, cookies)
        if response is None:
            logger.warning("Ошибка парсинга расписания в промежутке")
            return None
        return response.json()

    async def get_missed_lessons(self, cookies: dict) -> dict | None:
        url: str = "https://sh-open.ris61edu.ru/api/ScheduleService/GetMissedLessons"
        response: httpx.Response | None = await self.__request(url, cookies)
        if response is None:
            logger.warning("Ошибка парсинга пропущенных уроков")
            return None
        return response.json()
