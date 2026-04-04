from typing import List
import uuid

from fastapi import APIRouter
from sqlmodel import Session

from app.db.database import get_db_interface, FoodPairing


ROUTER = APIRouter(
    prefix="/food_pairings"
)


@ROUTER.get("/", status_code=200)
def get_food_pairings() -> List[FoodPairing]:
    food_pairings: List[FoodPairing] = []
    with Session(get_db_interface().engine) as session:
        food_pairings = session.query(FoodPairing).all()
    return food_pairings


@ROUTER.post("/", status_code=201)
def create_food_pairing(food_pairing: FoodPairing) -> str:
    for key, value in vars(food_pairing).items():
        if key == "pairing_id":
            setattr(food_pairing, key, str(uuid.uuid4()))
        elif value is None or value == "string":
            setattr(food_pairing, key, None)
    with Session(get_db_interface().engine) as session:
        session.add(food_pairing)
        session.commit()
        session.refresh(food_pairing)
    return "OK"