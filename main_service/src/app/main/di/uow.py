from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.uow import UoW
from app.main.di.stub import Stub


def get_uow(
        session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
) -> UoW:
    return UoW(session)
