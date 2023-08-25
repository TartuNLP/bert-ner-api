from typing import Any
import logging

from fastapi import APIRouter
class EndpointFilter(logging.Filter):
    def __init__(
        self,
        path: str,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._path = path

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find(self._path) == -1
    
health_router = APIRouter(tags=["health"])

@health_router.get('/readiness')
@health_router.get('/startup')
@health_router.get('/liveness')
async def health_check():
    return "OK"

uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.addFilter(EndpointFilter(path="/health/"))

