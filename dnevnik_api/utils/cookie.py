import json
from typing import Any
import threading
from pathlib import Path
import logging

logger: logging.Logger = logging.getLogger(__name__)


class Cookie:
    def __init__(self, cookie_path: Path, delete_interval: float = 300.0) -> None:
        self.__cookie_path: Path = cookie_path
        self.__delete_interval: float = delete_interval

    def __delete_cookie_file(self, file_path) -> None:
        try:
            if file_path.exists():
                file_path.unlink()
                logger.info(
                    f"Cookie file {file_path} automatically deleted after {self.__delete_interval // 60} minutes"
                )
        except Exception as e:
            logger.error(f"Error deleting cookie file {file_path}: {e}")

    def save_cookies(self, cookies: list[dict[str, Any]], name: str) -> bool:
        try:
            file_path: Path = Path(self.__cookie_path) / name
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(cookies, file, indent=2, ensure_ascii=False)

            logger.info(f"Cookies saved to {file_path}")

            timer = threading.Timer(self.__delete_interval, self.__delete_cookie_file, [file_path])
            timer.start()

            return True

        except Exception as e:
            logger.error(f"Error saving cookies to {file_path}: {e}")
            return False

    def load_cookies(self, name: str) -> list[dict[str, Any]]:
        try:
            file_path: Path = Path(self.__cookie_path) / name

            if not file_path.exists():
                logger.warning(f"Cookies file not found: {file_path}")
                return []

            with open(file_path, "r", encoding="utf-8") as file:
                cookies = json.load(file)

            logger.info(f"Cookies loaded from {file_path}")
            return cookies

        except Exception as e:
            logger.error(f"Error loading cookies from {file_path}: {e}")
            return []
