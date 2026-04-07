from typing import List
import uuid

from fastapi import APIRouter
from sqlmodel import Session

from app.db.database import get_db_interface, GrapeVariety


ROUTER = APIRouter(
    prefix="/grape_varieties",
    tags=["grape_varieties"]
)


@ROUTER.get("/", status_code=200)
def get_grape_varieties() -> List[GrapeVariety]:
    grape_varieties: List[GrapeVariety] = []
    with Session(get_db_interface().engine) as session:
        grape_varieties = session.query(GrapeVariety).all()
    return grape_varieties


@ROUTER.post("/", status_code=201)
def create_grape_variety(grape_variety: GrapeVariety) -> str:
    for key, value in vars(grape_variety).items():
        if key == "variety_id":
            setattr(grape_variety, key, str(uuid.uuid4()))
        elif value is None or value == "string":
            setattr(grape_variety, key, None)
    with Session(get_db_interface().engine) as session:
        session.add(grape_variety)
        session.commit()
        session.refresh(grape_variety)
    return "OK"
