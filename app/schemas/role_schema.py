from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RoleCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    descripcion: str | None = Field(default=None, max_length=255)


class RoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: str | None
    creado_en: datetime
    actualizado_en: datetime
