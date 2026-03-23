from pydantic import BaseModel, ConfigDict


class RolePermissionCreate(BaseModel):
    rol_id: int
    permiso_id: int


class RolePermissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    rol_id: int
    permiso_id: int
