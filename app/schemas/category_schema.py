from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    tienda_id: int
    nombre: str = Field(min_length=2, max_length=80)
    descripcion: str | None = Field(default=None, max_length=255)
    activo: bool = True


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tienda_id: int
    nombre: str
    descripcion: str | None
    activo: bool
