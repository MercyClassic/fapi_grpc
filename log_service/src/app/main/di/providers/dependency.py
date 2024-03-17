import os
from typing import AsyncGenerator

from aiokafka import AIOKafkaProducer
from app.application.interfaces.services.file import FileServiceInterface
from app.application.services.file import FileService
from app.infrastructure.database.database import create_engine
from app.infrastructure.database.interfaces.repositories.file import (
    FileRepositoryInterface,
)
from app.infrastructure.database.repositories.file import FileRepository
from dishka import Provider, Scope, provide
from odmantic import AIOEngine
from odmantic.session import AIOSession


class DependencyProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def get_bus_producer(self) -> AsyncGenerator[AIOKafkaProducer, None]:
        producer = AIOKafkaProducer(
            bootstrap_servers=os.environ['KAFKA_BOOTSTRAP_SERVER'],
        )
        await producer.start()
        try:
            yield producer
        finally:
            await producer.stop()

    @provide(scope=Scope.APP)
    def get_engine(self) -> AIOEngine:
        engine = create_engine(
            db_uri=os.environ['mongo_db_uri'],
            db_name=os.environ['mongo_db_name'],
        )
        return engine

    @provide()
    async def get_session(self, engine: AIOEngine) -> AsyncGenerator[AIOSession, None]:
        async with engine.session() as session:
            yield session

    @provide()
    def get_file_repository(
            self,
            session: AIOSession,
    ) -> FileRepositoryInterface:
        return FileRepository(session=session)

    @provide()
    def get_file_service(
            self,
            file_repo: FileRepositoryInterface,
            bus_producer: AIOKafkaProducer,
    ) -> FileServiceInterface:
        return FileService(file_repo=file_repo, bus_producer=bus_producer)
