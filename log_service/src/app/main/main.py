import asyncio
import logging

from app.application.grpc import log_file_service_pb2_grpc
from app.main.di.provider import DependencyProvider
from app.main.server import LogFileServicer
from dishka import make_async_container

from grpc import aio

logging.basicConfig(
    level=logging.INFO,
    format='{asctime} - [{levelname}] - {name} - {funcName}:{lineno} - {message}',
    style='{',
    datefmt='%Y-%m-%d %H:%M:%S',
)


async def main() -> None:
    provider = DependencyProvider()
    container = make_async_container(provider)

    server = aio.server()
    log_file_servicer = LogFileServicer(container=container)
    log_file_service_pb2_grpc.add_LogFileServiceServicer_to_server(log_file_servicer, server)
    server.add_insecure_port('0.0.0.0:8001')
    await server.start()
    await server.wait_for_termination()
    await container.close()


if __name__ == '__main__':
    asyncio.run(main())
