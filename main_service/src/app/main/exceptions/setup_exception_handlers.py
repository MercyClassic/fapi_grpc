import json
import logging
from functools import partial

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.domain.exceptions.file import FileNotFound

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(Exception, unexpected_error_log)
    app.add_exception_handler(
        FileNotFound,
        partial(
            error_handler,
            error_info='File Not Found',
            status_code=404,
        ),
    )


def get_error_handler(error_info: str, status_code: int):
    return partial(
        error_handler,
        error_info=error_info,
        status_code=status_code,
    )


def error_handler(
    request: Request,
    ex: Exception,
    error_info: str,
    status_code: int,
) -> JSONResponse:
    logger.error(ex, exc_info=True)
    return JSONResponse(
        status_code=status_code,
        content=json.dumps({'detail': error_info}),
    )


async def unexpected_error_log(request: Request, ex: Exception) -> JSONResponse:
    logger.error(ex, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content='Something went wrong',
    )