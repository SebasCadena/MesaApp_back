from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ReservaEstado


class ReservationCreate(BaseModel):
    tienda_id: int
    mesa_id: int
    nombre_cliente: str = Field(min_length=2, max_length=120)
    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime
    estado: ReservaEstado = ReservaEstado.ACTIVA
    creado_por_usuario_id: int | None = None


class ReservationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tienda_id: int
    mesa_id: int
    nombre_cliente: str
    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime
    estado: ReservaEstado
    creado_por_usuario_id: int | None
    creado_en: datetime
    actualizado_en: datetime
