import enum
from uuid import UUID

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base


class StatusEnum(enum.Enum):
    failed = 'failed'
    in_process = 'in_process'
    success = 'success'


class File(Base):
    __tablename__ = 'file'

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum).values_callable,
        default=False,
    )
