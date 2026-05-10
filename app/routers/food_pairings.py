from typing import List
import uuid
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.logging_config import LOGGER_NAME
from app.db.database import get_db_interface, FoodPairing, SupplyFoodPairingLink


class FoodPairingCreate(BaseModel):
    name: str
    description: str | None = None


ROUTER = APIRouter(
    prefix="/food_pairings",
    tags=["food_pairings"]
)


@ROUTER.get("/", status_code=200)
def get_food_pairings(name: str | None = None, upc_vintage_sd_id: str | None = None) -> List[FoodPairing]:
    food_pairings: List[FoodPairing] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(FoodPairing)
        if name:
            stmt = stmt.where(FoodPairing.name.ilike(f"%{name}%"))
        if upc_vintage_sd_id:
            stmt = stmt.join(SupplyFoodPairingLink, FoodPairing.pairing_id == SupplyFoodPairingLink.pairing_id)
            stmt = stmt.where(SupplyFoodPairingLink.supply_id == upc_vintage_sd_id)
        food_pairings = session.exec(stmt).all()
    return food_pairings


@ROUTER.post("/", status_code=201)
def create_food_pairing(food_pairing: FoodPairing) -> str:
    food_pairings: List[FoodPairing] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(FoodPairing)
        stmt = stmt.where(FoodPairing.name == food_pairing.name)
        food_pairings = session.exec(stmt).all()
    if len(food_pairings) > 0:
        return food_pairings[0].pairing_id

    food_pairing_obj = FoodPairing(
        pairing_id=str(uuid.uuid4()),
        name=food_pairing.name,
        description=food_pairing.description
    )
    try:
        with Session(get_db_interface().engine) as session:
            session.add(food_pairing_obj)
            session.commit()
            session.refresh(food_pairing_obj)
    except Exception as exc:
        logger = logging.getLogger(LOGGER_NAME)
        logger.error(f"Error creating food pairing entry: {exc}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the food pairing entry.")
    return food_pairing_obj.pairing_id
