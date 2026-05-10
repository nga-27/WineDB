from typing import List
import uuid
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.logging_config import LOGGER_NAME
from app.db.database import get_db_interface, GrapeVariety, SupplyGrapeLink


class GrapeVarietyCreate(BaseModel):
    name: str
    description: str | None = None
    region_id: str | None = None


ROUTER = APIRouter(
    prefix="/grape_varieties",
    tags=["grape_varieties"]
)


@ROUTER.get("/", status_code=200)
def get_grape_varieties(name: str | None = None, upc_vintage_sd_id: str | None = None) -> List[GrapeVariety]:
    grape_varieties: List[GrapeVariety] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(GrapeVariety)
        if name:
            stmt = stmt.where(GrapeVariety.name.ilike(f"%{name}%"))
        if upc_vintage_sd_id:
            stmt = stmt.join(SupplyGrapeLink, GrapeVariety.variety_id == SupplyGrapeLink.variety_id)
            stmt = stmt.where(SupplyGrapeLink.supply_id == upc_vintage_sd_id)
        grape_varieties = session.exec(stmt).all()
    return grape_varieties


@ROUTER.post("/", status_code=201)
def create_grape_variety(grape_variety: GrapeVarietyCreate) -> str:
    grapes: List[GrapeVariety] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(GrapeVariety)
        stmt = stmt.where(GrapeVariety.name == grape_variety.name)
        grapes = session.exec(stmt).all()
    if len(grapes) > 0:
        return grapes[0].variety_id

    grape_variety_obj = GrapeVariety(
        variety_id=str(uuid.uuid4()),
        name=grape_variety.name,
        description=grape_variety.description,
        region_id=grape_variety.region_id
    )
    try:
        with Session(get_db_interface().engine) as session:
            session.add(grape_variety_obj)
            session.commit()
            session.refresh(grape_variety_obj)
    except Exception as exc:
        logger = logging.getLogger(LOGGER_NAME)
        logger.error(f"Error creating grape variety entry: {exc}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the grape variety entry.")
    return grape_variety_obj.variety_id
