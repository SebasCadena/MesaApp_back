from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    cedula: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=255)


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class AuthUserResponse(BaseModel):
    id: int
    nombre: str
    cedula: str
    correo: str
    tienda_id: int | None
    is_superadmin: bool
    roles: list[str]
    permisos: list[str]


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: AuthUserResponse


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class MeResponse(AuthUserResponse):
    pass