from typing import Annotated

from app.infrastructure.database.uow import UoW
from app.main.di.dependencies.stub import Stub
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_uow(
        session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
) -> UoW:
    return UoW(session)
