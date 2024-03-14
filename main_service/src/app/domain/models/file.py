from dataclasses import dataclass
from uuid import UUID

from app.domain.models.base import Entity


@dataclass
class FileEntity(Entity):
    uuid: UUID | None
    status: str
    data: dict | None
