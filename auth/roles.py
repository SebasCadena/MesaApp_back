from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.permission_model import Permission
from app.models.role_model import Role
from app.models.role_permission_model import RolePermission
from app.models.user_role_model import UserRole
from auth.bearer import get_current_token_payload
from config.config import get_db


SUPERADMIN_ROLE_NAME = "superadmin"

def get_user_security_context(db: Session, user_id: int) -> dict:
    """Resuelve tienda, roles y permisos activos del usuario desde BD."""
    rows = (
        db.query(UserRole.tienda_id, Role.nombre, Permission.nombre)
        .join(Role, Role.id == UserRole.rol_id)
        .outerjoin(RolePermission, RolePermission.rol_id == Role.id)
        .outerjoin(Permission, Permission.id == RolePermission.permiso_id)
        .filter(UserRole.usuario_id == user_id, UserRole.activo.is_(True))
        .all()
    )

    if not rows:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario no tiene roles activos",
        )

    roles = sorted({row[1] for row in rows if row[1]})
    permissions = sorted({row[2] for row in rows if row[2]})
    store_ids = sorted({row[0] for row in rows if row[0] is not None})

    is_superadmin = any(role.lower() == SUPERADMIN_ROLE_NAME for role in roles)
    if len(store_ids) > 1 and not is_superadmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario tiene múltiples tiendas activas y no es superadmin",
        )

    return {
        "store_id": store_ids[0] if store_ids else None,
        "roles": roles,
        "permissions": permissions,
        "is_superadmin": is_superadmin,
    }

def get_current_security_context(
    payload: dict = Depends(get_current_token_payload),
    db: Session = Depends(get_db),
) -> dict:
    """Carga el contexto de seguridad y valida coherencia básica con el token."""
    user_id = payload.get("sub")
    try:
        user_id_int = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    context = get_user_security_context(db=db, user_id=user_id_int)

    token_store_id = payload.get("store_id")
    if not context["is_superadmin"] and token_store_id is not None:
        try:
            token_store_id_int = int(token_store_id)
        except (TypeError, ValueError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        if context["store_id"] != token_store_id_int:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token fuera de contexto de tienda",
            )

    context["user_id"] = user_id_int
    return context

def require_permissions(required_permissions: list[str]):
    """Dependencia para proteger rutas por permisos (RBAC)."""

    def dependency(context: dict = Depends(get_current_security_context)) -> dict:
        if context["is_superadmin"]:
            return context

        user_permissions = set(context["permissions"])
        missing = [perm for perm in required_permissions if perm not in user_permissions]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permisos insuficientes. Faltan: {', '.join(missing)}",
            )
        return context

    return dependency