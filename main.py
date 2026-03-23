from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    app_setting_router,
    category_router,
    inventory_movement_router,
    material_router,
    order_detail_router,
    order_router,
    payment_router,
    permission_router,
    product_material_router,
    product_router,
    reservation_router,
    role_permission_router,
    role_router,
    store_router,
    store_setting_router,
    table_router,
    user_role_router,
    user_router,
    auth_router
)

app = FastAPI(title="MesaApp API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "MesaApp API"}


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


app.include_router(store_router)
app.include_router(app_setting_router)
app.include_router(store_setting_router)
app.include_router(inventory_movement_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(material_router)
app.include_router(product_material_router)
app.include_router(table_router)
app.include_router(reservation_router)
app.include_router(order_router)
app.include_router(order_detail_router)
app.include_router(payment_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(permission_router)
app.include_router(role_permission_router)
app.include_router(user_role_router)
app.include_router(auth_router)