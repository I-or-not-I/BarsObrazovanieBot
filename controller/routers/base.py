from fastapi import APIRouter
from routers.abstract import AbstractRouter


class BaseRouter(AbstractRouter):
    def __init__(self, register_paths: tuple) -> None:
        self._register_paths: tuple = register_paths
        self._router: APIRouter = APIRouter()
        self._routs_register(register_paths)

    def _routs_register(self, register_paths: tuple) -> None:
        for path, endpoint, methods in register_paths:
            self._router.add_api_route(path, endpoint, methods=methods)

    def get_router(self) -> APIRouter:
        return self._router

    def get_endpoints(self) -> list:
        return [path_data[0] for path_data in self._register_paths]
