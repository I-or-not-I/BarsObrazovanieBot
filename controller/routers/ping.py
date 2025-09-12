from routers.base import BaseRouter


class Router(BaseRouter):
    def __init__(self) -> None:
        register_paths: tuple = (("/", self.__ping, ["GET"]),)
        super().__init__(register_paths)

    async def __ping(self) -> str:
        return "PONG"
