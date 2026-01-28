import logging

from app.presentators.api.root_router import root_router
from fastapi import FastAPI

from app.main.di.init_dependencies import init_dependencies
from app.main.setup_exception_handlers import setup_exception_handlers

logging.basicConfig(
    level=logging.INFO,
    format='{asctime} - [{levelname}] - {name} - {funcName}:{lineno} - {message}',
    style='{',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def create_app() -> FastAPI:
    app = FastAPI()
    setup_exception_handlers(app)
    init_dependencies(app)
    app.include_router(root_router)
    return app


app = create_app()
