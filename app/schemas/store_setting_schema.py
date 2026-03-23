from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StoreSettingCreate(BaseModel):
    tienda_id: int
    clave: str = Field(min_length=2, max_length=100)
    valor: str | None = None
    tipo_valor: str = Field(default="string", min_length=2, max_length=20)
    descripcion: str | None = Field(default=None, max_length=255)
    editable: bool = True
    actualizado_por_usuario_id: int | None = None


class StoreSettingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tienda_id: int
    clave: str
    valor: str | None
    tipo_valor: str
    descripcion: str | None
    editable: bool
    actualizado_por_usuario_id: int | None
    actualizado_en: datetime
