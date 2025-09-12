"""
Основной модуль запуска FastAPI сервера для образовательного бота.
"""

from os import environ
from json import loads
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import Config, Server
from sqlalchemy.ext.asyncio import async_sessionmaker

from routers import abstract
from routers import ping
from routers.admin import admin
from utils.logger import Logger
from src.db import AbstractDb, Database


from config import PARSER_IP, LOGGING_LEVEL, HOST, PORT, TIMEOUT, DB_DATA


async def main() -> None:
    Logger(LOGGING_LEVEL)

    app: FastAPI = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    db: AbstractDb = Database(DB_DATA)
    await db.create_tables()
    session_factory: async_sessionmaker = await db.get_session_factory()

    routers: tuple[abstract.AbstractRouter, ...] = (
        ping.Router(),
        admin.Router(session_factory),
    )
    for router in routers:
        app.include_router(router.get_router())

    config = Config(app, host=HOST, port=PORT)
    server = Server(config=config)
    await server.serve()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
