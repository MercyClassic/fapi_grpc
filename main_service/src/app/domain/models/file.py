from uuid import UUID

from app.domain.models.base import Entity


class FileEntity(Entity):
    uuid: UUID | None
    data: dict
