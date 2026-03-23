from fastapi import FastAPI

from app.routers import store_router

app = FastAPI(title="MesaApp API")


@app.get("/")
def read_root():
    return {"message": "MesaApp API"}


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


app.include_router(store_router)
