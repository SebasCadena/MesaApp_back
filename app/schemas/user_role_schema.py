from datetime import date

from pydantic import BaseModel, ConfigDict


class UserRoleCreate(BaseModel):
    usuario_id: int
    rol_id: int
    tienda_id: int
    salario: float | None = None
    fecha_contrato: date | None = None
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    activo: bool = True


class UserRoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    rol_id: int
    tienda_id: int
    salario: float | None
    fecha_contrato: date | None
    fecha_inicio: date
    fecha_fin: date | None
    activo: bool
