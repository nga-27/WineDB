from typing import List
import uuid

from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import Session

from app.db.database import (
    get_db_interface,
    WineSupply,
    GrapeVariety,
    FoodPairing,
)


class WineSupplyCreate(BaseModel):
    name: str
    quantity: int
    upc_vintage_sd_id: str | None = None
    upc_barcode_id: str | None = None
    vintage: str | None = None
    vendor: str | None = None
    region: str | None = None
    pct_alcohol: str | None = None
    drink_by_date: str | None = None
    tasting_notes: str | None = None
    obtainment_note: str | None = None
    other_notes: str | None = None
    physical_location_id: str | None = None
    wine_type_id: str | None = None
    country_id: str | None = None
    drank_event_notes: str | None = None
    drank_date: str | None = None
    grape_ids: list[str] = []
    food_pairing_ids: list[str] = []


ROUTER = APIRouter(
    prefix="/wine_supplies"
)


@ROUTER.get("/", status_code=200)
def get_wine_supplies() -> List[WineSupply]:
    wine_supplies: List[WineSupply] = []
    with Session(get_db_interface().engine) as session:
        wine_supplies = session.query(WineSupply).all()
    return wine_supplies


@ROUTER.post("/", status_code=201)
def create_wine_supply(wine_supply: WineSupplyCreate) -> str:
    if not wine_supply.upc_vintage_sd_id:
        wine_supply.upc_vintage_sd_id = str(uuid.uuid4())

    db_supply = WineSupply(
        upc_vintage_sd_id=wine_supply.upc_vintage_sd_id,
        name=wine_supply.name,
        quantity=wine_supply.quantity,
        upc_barcode_id=wine_supply.upc_barcode_id,
        vintage=wine_supply.vintage,
        vendor=wine_supply.vendor,
        region=wine_supply.region,
        pct_alcohol=wine_supply.pct_alcohol,
        drink_by_date=wine_supply.drink_by_date,
        tasting_notes=wine_supply.tasting_notes,
        obtainment_note=wine_supply.obtainment_note,
        other_notes=wine_supply.other_notes,
        physical_location_id=wine_supply.physical_location_id,
        wine_type_id=wine_supply.wine_type_id,
        country_id=wine_supply.country_id,
        drank_event_notes=wine_supply.drank_event_notes,
        drank_date=wine_supply.drank_date,
    )

    with Session(get_db_interface().engine) as session:
        db_supply.grapes = [session.get(GrapeVariety, grape_id) for grape_id in wine_supply.grape_ids if grape_id]
        db_supply.food_pairings = [session.get(FoodPairing, pairing_id) for pairing_id in wine_supply.food_pairing_ids if pairing_id]

        session.add(db_supply)
        session.commit()
        session.refresh(db_supply)

    return "OK"