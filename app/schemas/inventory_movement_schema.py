from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums import TipoMovimientoInventario


class InventoryMovementCreate(BaseModel):
    tienda_id: int
    material_id: int | None = None
    producto_id: int | None = None
    tipo_movimiento: TipoMovimientoInventario
    cantidad: float = Field(gt=0)
    motivo: str | None = Field(default=None, max_length=255)
    creado_por_usuario_id: int | None = None

    @model_validator(mode="after")
    def validate_target(self) -> "InventoryMovementCreate":
        if self.material_id is None and self.producto_id is None:
            raise ValueError("Debes enviar material_id o producto_id")
        return self


class InventoryMovementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tienda_id: int
    material_id: int | None
    producto_id: int | None
    tipo_movimiento: TipoMovimientoInventario
    cantidad: float
    motivo: str | None
    creado_por_usuario_id: int | None
    creado_en: datetime
