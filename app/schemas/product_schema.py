from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    tienda_id: int
    nombre: str = Field(min_length=2, max_length=120)
    descripcion: str | None = None
    precio: float = Field(gt=0)
    categoria_id: int
    img_url: str | None = None
    activo: bool = True
    stock: float = Field(default=0, ge=0)
    stock_minimo: float = Field(default=0, ge=0)
    usa_receta: bool = False


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tienda_id: int
    nombre: str
    descripcion: str | None
    precio: float
    categoria_id: int
    img_url: str | None
    activo: bool
    stock: float
    stock_minimo: float
    usa_receta: bool
    creado_en: datetime
    actualizado_en: datetime
