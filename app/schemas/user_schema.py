from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    cedula: str = Field(min_length=5, max_length=30)
    celular: str | None = Field(default=None, max_length=30)
    correo: str = Field(min_length=5, max_length=120)
    password_hash: str = Field(min_length=8, max_length=255)
    direccion: str | None = Field(default=None, max_length=255)
    fecha_nacimiento: date | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    cedula: str
    celular: str | None
    correo: str
    direccion: str | None
    fecha_nacimiento: date | None
    activo: bool
    creado_en: datetime
    actualizado_en: datetime
