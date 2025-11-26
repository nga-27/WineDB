from typing import List
import uuid

from fastapi import APIRouter
from sqlmodel import Session

from app.db.database import get_db_interface, Country


ROUTER = APIRouter(
    prefix="/countries"
)

@ROUTER.get("/", status_code=200)
def get_countries() -> List[Country]:
    countries: List[Country] = []
    with Session(get_db_interface().engine) as session:
        countries = session.query(Country).all()
    return countries


@ROUTER.post("/", status_code=201)
def create_country(country: Country) -> str:
    for key, value in vars(country).items():
        if key == "country_id":
            setattr(country, key, str(uuid.uuid4()))
        elif value is None or value == "string":
            setattr(country, key, None)
    with Session(get_db_interface().engine) as session:
        session.add(country)
        session.commit()
        session.refresh(country)
    return "OK"
