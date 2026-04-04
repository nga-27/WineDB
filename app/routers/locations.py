from typing import List
import uuid

from fastapi import APIRouter
from sqlmodel import Session

from app.db.database import get_db_interface, PhysicalLocation


ROUTER = APIRouter(
    prefix="/locations"
)


@ROUTER.get("/", status_code=200)
def get_locations() -> List[PhysicalLocation]:
    locations: List[PhysicalLocation] = []
    with Session(get_db_interface().engine) as session:
        locations = session.query(PhysicalLocation).all()
    return locations


@ROUTER.post("/", status_code=201)
def create_location(location: PhysicalLocation) -> str:
    for key, value in vars(location).items():
        if key == "location_id":
            setattr(location, key, str(uuid.uuid4()))
        elif value is None or value == "string":
            setattr(location, key, None)
    with Session(get_db_interface().engine) as session:
        session.add(location)
        session.commit()
        session.refresh(location)
    return "OK"
