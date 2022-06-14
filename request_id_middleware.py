# coding:utf-8

import logging
from contextvars import ContextVar
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp


LOGGER_CONF_FILE_PATH = "logging.conf"

_request_id_var: ContextVar[str] = ContextVar("request_id")


def get_request_id() -> str:
    return _request_id_var.get()


class RequestIDMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        logging.config.fileConfig(LOGGER_CONF_FILE_PATH)
        self.logger = logging.getLogger("requestIDLogger")  # 初始化logger

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        request_id = _request_id_var.set(str(uuid4()))

        response = await call_next(request)

        response.headers["X-Request-ID"] = get_request_id()

        message = "log for request, request id is: " + get_request_id() + " status code:" + str(response.status_code)
        self.logger.info(message)
        _request_id_var.reset(request_id)

        return response