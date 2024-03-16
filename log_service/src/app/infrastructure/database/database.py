from typing import Iterable

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from odmantic.session import AIOSession


def create_engine(db_uri: str, db_name: str) -> AIOEngine:
    client = AsyncIOMotorClient(db_uri)
    engine = AIOEngine(client=client, database=db_name)
    return engine


async def get_session(engine: AIOEngine) -> Iterable[AIOSession]:
    async with engine.session() as session:
        yield session
