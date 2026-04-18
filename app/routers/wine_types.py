from typing import List
import uuid
import logging

from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel

from app.logging_config import LOGGER_NAME
from app.db.database import get_db_interface, WineType


class CreateWineType(BaseModel):
    name: str
    description: str | None = None


ROUTER = APIRouter(
    prefix="/wine_types",
    tags=["wine_types"]
)


@ROUTER.get("/", status_code=200)
def get_wine_types(name: str | None = None) -> List[WineType]:
    wine_types: List[WineType] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(WineType)
        if name:
            stmt = stmt.where(WineType.name.ilike(f"%{name}%"))
        wine_types = session.exec(stmt).all()
    return wine_types


@ROUTER.post("/", status_code=201)
def create_wine_type(wine_type: CreateWineType) -> str:
    wine_types: List[WineType] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(WineType)
        stmt = stmt.where(WineType.name == wine_type.name)
        wine_types = session.exec(stmt).all()
    if len(wine_types) > 0:
        return wine_types[0].type_id

    wine_type_entry = WineType(
        name=wine_type.name,
        description=wine_type.description,
        type_id=str(uuid.uuid4())
    )
    try:
        with Session(get_db_interface().engine) as session:
            session.add(wine_type_entry)
            session.commit()
            session.refresh(wine_type_entry)
    except Exception as exc:
        logger = logging.getLogger(LOGGER_NAME)
        logger.error(f"Error creating wine type entry: {exc}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the wine type entry.")
    return wine_type_entry.type_id
