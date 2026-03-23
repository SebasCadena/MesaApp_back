from pydantic import BaseModel, ConfigDict, Field


class OrderDetailCreate(BaseModel):
    pedido_id: int
    producto_id: int
    cantidad: float = Field(gt=0)
    precio_unitario: float = Field(ge=0)
    subtotal_linea: float = Field(ge=0)


class OrderDetailRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pedido_id: int
    producto_id: int
    cantidad: float
    precio_unitario: float
    subtotal_linea: float
