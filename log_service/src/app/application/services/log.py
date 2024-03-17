import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import Iterator

from app.application.interfaces.services.log import LogFileServiceInterface
from app.application.interfaces.services.main_file import MainFileServiceInterface
from app.domain.models.file import FileEntity


def get_logger() -> logging.Logger:
    formatter = logging.Formatter(
        fmt='[{levelname}] - {message}',
        style='{',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    warning_formatter = logging.Formatter(
        fmt='[{levelname}]: File[{file_uuid}] - {message}',
        style='{',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    warning_handler = logging.StreamHandler()
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(warning_formatter)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    handler.addFilter(lambda record: record.levelno == logging.INFO)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.addHandler(warning_handler)
    return logger


logger = get_logger()


class LogFileService(LogFileServiceInterface):
    def __init__(self, main_file_service: MainFileServiceInterface) -> None:
        self._main_file_service = main_file_service
        self.WARNING_KEYS = ('warning', 'warn', 'deprecated')
        self.ERROR_KEYS = ('error', 'forbidden')

    def recursive_items(self, dictionary: dict) -> Iterator[str]:
        for key, value in dictionary.items():
            if isinstance(value, dict):
                yield key
                yield from self.recursive_items(value)
            else:
                yield key

    async def process_logging(self, file: FileEntity, dt: datetime) -> None:
        logger.info(
            f'Processing file with uuid: {file.uuid}\n'
            f'UTC time: {dt}\n'
            f'Moscow time: {dt + timedelta(hours=3)}\n'
            f'File data: {file.data}\n',
        )
        await asyncio.sleep(random.randint(3, 7))

        status = 'success'
        keys = self.recursive_items(file.data)
        for key in keys:
            if key in self.WARNING_KEYS:
                logger.warning(
                    f'Key "{key}" in WARNING keys',
                    extra={'file_uuid': file.uuid},
                )
            elif key in self.ERROR_KEYS:
                logger.error(
                    f'Key "{key}" in ERROR keys, process failed',
                    extra={'file_uuid': file.uuid},
                )
                status = 'failed'
                break
        logger.info(f'File [{file.uuid}] process finished, status: {status}\n')
        await self._main_file_service.update_file(file_uuid=file.uuid, status=status)
