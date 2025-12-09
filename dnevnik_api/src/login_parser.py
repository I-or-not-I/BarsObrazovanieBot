import logging
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional, AsyncIterator

import aiohttp
from eel import sleep
from flask import request
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import asyncio

from utils.cookie import Cookie

logger: logging.Logger = logging.getLogger(__name__)


class AbstractLoginParser(ABC):
    @abstractmethod
    async def login(self, login: str, password: str) -> bool:
        pass

    @abstractmethod
    async def sms_login(self, sms_code: str) -> Optional[dict]:
        pass


class LoginParser(AbstractLoginParser):
    DEFAULT_TIMEOUT = 30.0
    LOGIN_URL = "https://sh-open.ris61edu.ru/auth/esia/send-authn-request"
    VERIFY_URL = "https://esia.gosuslugi.ru/aas/oauth2/api/login/otp/verify"
    MAX_SKIP_URL = "https://esia.gosuslugi.ru/aas/oauth2/api/login/quiz-max/skip"
    PERSONAL_AREA_URL = "https://sh-open.ris61edu.ru/personal-area"

    LOGIN_INPUT_LOCATOR = (By.ID, "login")
    PASSWORD_INPUT_LOCATOR = (By.ID, "password")
    PERSONAL_AREA_LINK_LOCATOR = (By.XPATH, "/html/body/section/section[1]/div/section[2]/div/a")

    def __init__(self, timeout: float = DEFAULT_TIMEOUT, cookie_path: str = "cookies") -> None:
        self.__timeout = timeout
        self.__cookie = Cookie(Path(cookie_path))

    def __create_browser(self) -> WebDriver:
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--disable-dev-shm-usage")

        return webdriver.Chrome(options=chrome_options)

    @asynccontextmanager
    async def __browser_context(self) -> AsyncIterator[WebDriver]:
        browser: WebDriver | None = None
        try:
            browser = await asyncio.get_event_loop().run_in_executor(None, self.__create_browser)
            if browser is None:
                raise RuntimeError("Failed to create browser instance")
            yield browser
        except Exception as e:
            logger.error(f"Failed to create browser: {str(e)}")
            raise
        finally:
            if browser is not None:
                await asyncio.get_event_loop().run_in_executor(None, browser.quit)

    async def __wait_for_page_load(self, browser: WebDriver) -> None:
        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: WebDriverWait(browser, self.__timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            ),
        )

    async def __find_clickable_element(self, browser: WebDriver, locator: tuple) -> WebElement:
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: WebDriverWait(browser, self.__timeout).until(EC.element_to_be_clickable(locator))
        )

    async def __browser_get(self, browser: WebDriver, url: str) -> None:
        await asyncio.get_event_loop().run_in_executor(None, browser.get, url)

    async def __element_clear(self, element: WebElement) -> None:
        await asyncio.get_event_loop().run_in_executor(None, element.clear)

    async def __element_send_keys(self, element: WebElement, keys: str) -> None:
        await asyncio.get_event_loop().run_in_executor(None, element.send_keys, keys)

    async def __browser_get_cookies(self, browser: WebDriver) -> list:
        return await asyncio.get_event_loop().run_in_executor(None, browser.get_cookies)

    async def __browser_add_cookie(self, browser: WebDriver, cookie: dict) -> None:
        await asyncio.get_event_loop().run_in_executor(None, browser.add_cookie, cookie)

    async def __browser_refresh(self, browser: WebDriver) -> None:
        await asyncio.get_event_loop().run_in_executor(None, browser.refresh)

    async def __element_click(self, element: WebElement) -> None:
        await asyncio.get_event_loop().run_in_executor(None, element.click)

    async def __browser_execute_script(self, browser: WebDriver, script: str) -> str:
        return await asyncio.get_event_loop().run_in_executor(None, browser.execute_script, script)

    async def __browser_get_cookie(self, browser: WebDriver, name: str) -> Optional[dict]:
        all_cookies = await self.__browser_get_cookies(browser)
        return next((c for c in all_cookies if c.get("name") == name), None)

    async def login(self, login: str, password: str) -> bool:
        try:
            async with self.__browser_context() as browser:
                await self.__browser_get(browser, self.LOGIN_URL)
                await self.__wait_for_page_load(browser)

                login_input: WebElement = await self.__find_clickable_element(browser, self.LOGIN_INPUT_LOCATOR)
                await self.__element_clear(login_input)
                await self.__element_send_keys(login_input, login)

                password_input: WebElement = await self.__find_clickable_element(browser, self.PASSWORD_INPUT_LOCATOR)
                await self.__element_clear(password_input)
                await self.__element_send_keys(password_input, password + Keys.ENTER)

                await self.__wait_for_page_load(browser)

                cookies = await self.__browser_get_cookies(browser)
                await asyncio.get_event_loop().run_in_executor(None, self.__cookie.save_cookies, cookies, "user_name")
                logger.info("Login successful")
                return True

        except (TimeoutException, WebDriverException) as e:
            logger.error(f"Login failed: {str(e)}")
            return False

    async def sms_login(self, sms_code: str) -> Optional[dict]:
        try:
            async with self.__browser_context() as browser:
                await self.__browser_get(browser, "https://esia.gosuslugi.ru/login/")
                cookies = await asyncio.get_event_loop().run_in_executor(None, self.__cookie.load_cookies, "user_name")

                for cookie in cookies:
                    try:
                        if "expiry" in cookie:
                            cookie["expiry"] = int(cookie["expiry"])
                        await self.__browser_add_cookie(browser, cookie)
                    except Exception as e:
                        logger.warning(f"Failed to add cookie: {str(e)}")

                await self.__browser_refresh(browser)

                async with aiohttp.ClientSession() as session:
                    browser_cookies = {c["name"]: c["value"] for c in await self.__browser_get_cookies(browser)}

                    user_agent = await self.__browser_execute_script(browser, "return navigator.userAgent;")

                    headers = {
                        "Content-Type": "application/json",
                        "Accept": "application/json, text/plain, */*",
                        "User-Agent": user_agent,
                        "Origin": "https://esia.gosuslugi.ru",
                        "Referer": "https://esia.gosuslugi.ru/login/",
                    }

                    verify_url: str = f"{self.VERIFY_URL}?code={sms_code}"
                    async with session.post(verify_url, headers=headers, cookies=browser_cookies) as response:
                        if response.status != 200 and response.status != 202:
                            logger.warning(f"Verify request failed with status: {response.status}")
                    async with session.post(self.MAX_SKIP_URL, headers=headers, cookies=browser_cookies) as response:
                        if response.status != 200:
                            logger.warning(f"Verify request failed with status: {response.status}")

                await self.__browser_get(browser, self.PERSONAL_AREA_URL)
                element: WebElement = await self.__find_clickable_element(browser, self.PERSONAL_AREA_LINK_LOCATOR)
                await self.__element_click(element)

                session_cookie = await self.__browser_get_cookie(browser, "sessionid")
                if session_cookie:
                    return {session_cookie["name"]: session_cookie["value"]}

                logger.warning("Session cookie not found")
                return None

        except (TimeoutException, WebDriverException) as e:
            logger.error(f"SMS login failed: {str(e)}")
            return None
