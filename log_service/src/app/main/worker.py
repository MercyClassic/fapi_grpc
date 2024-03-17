import asyncio
import json
import os
from datetime import datetime

from aiokafka.consumer import AIOKafkaConsumer
from app.application.interfaces.services.log import LogFileServiceInterface
from app.domain.models.file import FileEntity
from app.main.di.providers.log import LogServiceProvider
from dishka import Container, make_container


class LogConsumer:
    def __init__(
            self,
            container: Container,
            bootstrap_servers: str,
    ):
        self.LOGGER_TOPIC = 'logger_topic'
        self._container = container
        self._consumer = AIOKafkaConsumer(self.LOGGER_TOPIC, bootstrap_servers=bootstrap_servers)

    async def consume(self) -> None:
        try:
            await self._consumer.start()
            async for msg in self._consumer:
                if msg.topic == self.LOGGER_TOPIC:
                    self.process_logger(msg.value, msg.timestamp)
        finally:
            await self._consumer.stop()

    def process_logger(self, data: bytes, timestamp: int) -> None:
        loop = asyncio.get_event_loop()
        decoded = json.loads(data.decode())
        file = FileEntity(uuid=decoded['uuid'], data=decoded['data'])
        with self._container() as request_container:
            log_file_service = request_container.get(LogFileServiceInterface)
            loop.create_task(
                log_file_service.process_logging(
                    file=file,
                    dt=datetime.utcfromtimestamp(timestamp // 1000),
                ),
            )


async def main():
    container = make_container(LogServiceProvider())

    consumer = LogConsumer(container, os.environ['KAFKA_BOOTSTRAP_SERVER'])
    await consumer.consume()


if __name__ == '__main__':
    asyncio.run(main())
