from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StoreCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    slug: str = Field(min_length=2, max_length=120)
    nit: str | None = Field(default=None, max_length=40)
    telefono: str | None = Field(default=None, max_length=30)
    correo: str | None = Field(default=None, max_length=120)
    direccion: str | None = Field(default=None, max_length=255)
    ciudad: str | None = Field(default=None, max_length=80)
    pais: str = Field(default="CO", min_length=2, max_length=80)


class StoreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    slug: str
    nit: str | None
    telefono: str | None
    correo: str | None
    direccion: str | None
    ciudad: str | None
    pais: str
    activo: bool
    creado_en: datetime
    actualizado_en: datetime
