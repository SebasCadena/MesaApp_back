from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import PedidoEstado, PedidoTipo


class OrderCreate(BaseModel):
    tienda_id: int
    mesa_id: int | None = None
    tipo: PedidoTipo
    estado: PedidoEstado = PedidoEstado.PENDIENTE
    subtotal: float = Field(default=0, ge=0)
    impuesto: float = Field(default=0, ge=0)
    descuento: float = Field(default=0, ge=0)
    total: float = Field(default=0, ge=0)
    notas: str | None = None
    creado_por_usuario_id: int | None = None


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tienda_id: int
    mesa_id: int | None
    tipo: PedidoTipo
    estado: PedidoEstado
    subtotal: float
    impuesto: float
    descuento: float
    total: float
    notas: str | None
    creado_por_usuario_id: int | None
    fecha_creacion: datetime
    actualizado_en: datetime
