from typing import List
import uuid

from fastapi import APIRouter
from sqlmodel import Session

from app.db.database import get_db_interface, WineType


ROUTER = APIRouter(
    prefix="/wine_types",
    tags=["wine_types"]
)


@ROUTER.get("/", status_code=200)
def get_wine_types() -> List[WineType]:
    wine_types: List[WineType] = []
    with Session(get_db_interface().engine) as session:
        wine_types = session.query(WineType).all()
    return wine_types


@ROUTER.post("/", status_code=201)
def create_wine_type(wine_type: WineType) -> str:
    for key, value in vars(wine_type).items():
        if key == "type_id":
            setattr(wine_type, key, str(uuid.uuid4()))
        elif value is None or value == "string":
            setattr(wine_type, key, None)
    with Session(get_db_interface().engine) as session:
        session.add(wine_type)
        session.commit()
        session.refresh(wine_type)
    return "OK"
