from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Json


class FileIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data: Any


class FileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    data: Json
