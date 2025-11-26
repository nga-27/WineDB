import os
import signal
import datetime

from fastapi import FastAPI

from app.routers import grapes, countries, wine_types


app = FastAPI(title="WineDB API", version="1.0.0", description="API for WineDB application.")

app.include_router(grapes.ROUTER)
app.include_router(countries.ROUTER)
app.include_router(wine_types.ROUTER)


@app.get("/")
def read_root():
    return {"Time": datetime.datetime.now().isoformat()}


@app.get("/start")
def start_api() -> dict:
    return {"status": "API is up and running!"}

@app.get("/shutdown")
def shutdown_api() -> dict:
    # Sync data, run copier, then close out
    os.kill(os.getpid(), signal.SIGTERM)
    return {"status": "API is shutting down..."}
