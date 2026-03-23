from fastapi import FastAPI

from app.routers import (
    permission_router,
    role_permission_router,
    role_router,
    store_router,
    user_role_router,
    user_router,
)

app = FastAPI(title="MesaApp API")


@app.get("/")
def read_root():
    return {"message": "MesaApp API"}


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


app.include_router(store_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(permission_router)
app.include_router(role_permission_router)
app.include_router(user_role_router)
