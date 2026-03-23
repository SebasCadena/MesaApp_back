from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import MetodoPago


class PaymentCreate(BaseModel):
    tienda_id: int
    pedido_id: int
    monto: float = Field(gt=0)
    metodo_pago: MetodoPago
    referencia_externa: str | None = Field(default=None, max_length=120)
    creado_por_usuario_id: int | None = None


class PaymentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tienda_id: int
    pedido_id: int
    monto: float
    metodo_pago: MetodoPago
    referencia_externa: str | None
    fecha: datetime
    creado_por_usuario_id: int | None
