from typing import List, Union
import uuid
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.logging_config import LOGGER_NAME
from app.db.database import get_db_interface, Country


class CreateCountryRequest(BaseModel):
    name: str
    description: str | None


ROUTER = APIRouter(
    prefix="/countries",
    tags=["countries"]
)

@ROUTER.get("/", status_code=200)
def get_countries(name: Union[str, None] = None) -> List[Country]:
    countries: List[Country] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(Country)
        if name:
            stmt = stmt.where(Country.name.ilike(f"%{name}%"))
        countries = session.exec(stmt).all()
    return countries


@ROUTER.get("/{country_id}", status_code=200)
def get_country_by_id(country_id: str) -> Union[Country, None]:
    with Session(get_db_interface().engine) as session:
        stmt = select(Country).where(Country.country_id == country_id)
        country = session.exec(stmt).one_or_none()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@ROUTER.post("/", status_code=201)
def create_country(country: CreateCountryRequest) -> str:
    countries: List[Country] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(Country)
        stmt = stmt.where(Country.name == country.name)
        countries = session.exec(stmt).all()
    if len(countries) > 0:
        return countries[0].country_id

    country_obj = Country(
        country_id=str(uuid.uuid4()),
        name=country.name,
        description=country.description
    )
    try:
        with Session(get_db_interface().engine) as session:
            session.add(country_obj)
            session.commit()
            session.refresh(country_obj)
    except Exception as exc:
        logger = logging.getLogger(LOGGER_NAME)
        logger.error(f"Error creating country entry: {exc}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the country entry.")
    return country_obj.country_id
