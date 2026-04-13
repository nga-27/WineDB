from typing import List
import uuid

from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import Session, select

from app.db.database import get_db_interface, Region


class CreateRegionRequest(BaseModel):
    name: str
    country_id: str | None
    description: str | None


ROUTER = APIRouter(
    prefix="/regions",
    tags=["regions"]
)

@ROUTER.get("/", status_code=200)
def get_regions(name: str | None = None) -> List[Region]:
    regions: List[Region] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(Region)
        if name:
            stmt = stmt.where(Region.name.ilike(f"%{name}%"))
        regions = session.exec(stmt).all()
    return regions


@ROUTER.post("/", status_code=201)
def create_region(region: CreateRegionRequest) -> str:
    regions: List[Region] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(Region)
        stmt = stmt.where(Region.name == region.name)
        regions = session.exec(stmt).all()
    if len(regions) > 0:
        return regions[0].region_id

    region_obj = Region(
        region_id=str(uuid.uuid4()),
        name=region.name,
        country_id=region.country_id,
        description=region.description
    )
    with Session(get_db_interface().engine) as session:
        session.add(region_obj)
        session.commit()
        session.refresh(region_obj)
    return region_obj.region_id
