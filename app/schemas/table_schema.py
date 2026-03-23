from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import MesaEstado


class TableCreate(BaseModel):
    tienda_id: int
    numero: int = Field(gt=0)
    capacidad_minima: int = Field(gt=0)
    capacidad_maxima: int = Field(gt=0)
    estado: MesaEstado = MesaEstado.DISPONIBLE
    activo: bool = True


class TableRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tienda_id: int
    numero: int
    capacidad_minima: int
    capacidad_maxima: int
    estado: MesaEstado
    activo: bool
    creado_en: datetime
    actualizado_en: datetime
