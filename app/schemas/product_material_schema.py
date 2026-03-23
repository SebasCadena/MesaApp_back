from pydantic import BaseModel, ConfigDict, Field


class ProductMaterialCreate(BaseModel):
    producto_id: int
    material_id: int
    cantidad: float = Field(gt=0)


class ProductMaterialRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    producto_id: int
    material_id: int
    cantidad: float
