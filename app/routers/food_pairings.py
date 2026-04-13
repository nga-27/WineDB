from typing import List
import uuid

from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import Session, select

from app.db.database import get_db_interface, FoodPairing


class FoodPairingCreate(BaseModel):
    name: str
    description: str | None = None


ROUTER = APIRouter(
    prefix="/food_pairings",
    tags=["food_pairings"]
)


@ROUTER.get("/", status_code=200)
def get_food_pairings(name: str | None = None) -> List[FoodPairing]:
    food_pairings: List[FoodPairing] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(FoodPairing)
        if name:
            stmt = stmt.where(FoodPairing.name.ilike(f"%{name}%"))
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
    with Session(get_db_interface().engine) as session:
        session.add(food_pairing_obj)
        session.commit()
        session.refresh(food_pairing_obj)
    return food_pairing_obj.pairing_id
