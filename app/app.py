import logging
import os
import signal
import datetime
from importlib.metadata import version

from fastapi import FastAPI

from app.logging_config import configure_logging, LOGGER_NAME
from app.routers import grapes, countries, regions, wine_types, locations, wine_supplies, keywords, food_pairings

configure_logging()
logger = logging.getLogger(LOGGER_NAME)

async def lifespan(app: FastAPI):
    logger.info("WineDB API startup complete")
    try:
        yield
    finally:
        logger.info("WineDB API shutdown complete")

app = FastAPI(
    title="WineDB API",
    version=version("WineDB"),
    description="API for WineDB application.",
    lifespan=lifespan,
)

app.include_router(grapes.ROUTER)
app.include_router(countries.ROUTER)
app.include_router(regions.ROUTER)
app.include_router(wine_types.ROUTER)
app.include_router(locations.ROUTER)
app.include_router(wine_supplies.ROUTER)
app.include_router(keywords.ROUTER)
app.include_router(food_pairings.ROUTER)


@app.get("/")
def read_root():
    logger.info("GET /")
    return {"Time": datetime.datetime.now().isoformat()}


@app.get("/start")
def start_api() -> dict:
    logger.info("GET /start")
    return {"status": "API is up and running!"}


@app.get("/shutdown")
def shutdown_api() -> dict:
    logger.info("GET /shutdown")
    # Sync data, run copier, then close out
    os.kill(os.getpid(), signal.SIGTERM)
    return {"status": "API is shutting down..."}
