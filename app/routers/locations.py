from typing import List
import uuid

from fastapi import APIRouter
from sqlmodel import Session, select
from pydantic import BaseModel

from app.db.database import get_db_interface, PhysicalLocation


class PhysicalLocationCreate(BaseModel):
    name: str
    description: str | None = None


ROUTER = APIRouter(
    prefix="/locations",
    tags=["locations"]
)


@ROUTER.get("/", status_code=200)
def get_locations(name: str | None = None) -> List[PhysicalLocation]:
    locations: List[PhysicalLocation] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(PhysicalLocation)
        if name:
            stmt = stmt.where(PhysicalLocation.name.ilike(f"%{name}%"))
        locations = session.exec(stmt).all()
    return locations


@ROUTER.post("/", status_code=201)
def create_location(location: PhysicalLocationCreate) -> str:
    locations: List[PhysicalLocation] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(PhysicalLocation)
        stmt = stmt.where(PhysicalLocation.name == location.name)
        locations = session.exec(stmt).all()
    if len(locations) > 0:
        return locations[0].location_id

    location_obj = PhysicalLocation(
        location_id=str(uuid.uuid4()),
        name=location.name,
        description=location.description
    )
    with Session(get_db_interface().engine) as session:
        session.add(location_obj)
        session.commit()
        session.refresh(location_obj)
    return location_obj.location_id
