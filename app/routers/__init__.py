from app.routers.category_router import router as category_router
from app.routers.material_router import router as material_router
from app.routers.permission_router import router as permission_router
from app.routers.product_material_router import router as product_material_router
from app.routers.product_router import router as product_router
from app.routers.role_permission_router import router as role_permission_router
from app.routers.role_router import router as role_router
from app.routers.store_router import router as store_router
from app.routers.user_role_router import router as user_role_router
from app.routers.user_router import router as user_router

__all__ = [
	"store_router",
	"category_router",
	"product_router",
	"material_router",
	"product_material_router",
	"user_router",
	"role_router",
	"permission_router",
	"role_permission_router",
	"user_role_router",
]
