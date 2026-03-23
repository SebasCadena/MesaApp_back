from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MaterialCreate(BaseModel):
    tienda_id: int
    nombre: str = Field(min_length=2, max_length=120)
    unidad: str = Field(min_length=1, max_length=20)
    stock: float = Field(default=0, ge=0)
    stock_minimo: float = Field(default=0, ge=0)


class MaterialRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tienda_id: int
    nombre: str
    unidad: str
    stock: float
    stock_minimo: float
    creado_en: datetime
    actualizado_en: datetime
