from typing import List
import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

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

class WineSupplyQuantityUpdate(BaseModel):
    bottle_id: str
    new_quantity: int


ROUTER = APIRouter(
    prefix="/wine_supplies",
    tags=["wine_supplies"]
)


@ROUTER.get("/", status_code=200)
def get_wine_supplies(name: str | None = None, vintage: str | None = None) -> List[WineSupply]:
    wine_supplies: List[WineSupply] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(WineSupply)
        if name:
            stmt = stmt.where(WineSupply.name.ilike(f"%{name}%"))
        if vintage:
            stmt = stmt.where(WineSupply.vintage == vintage)
        wine_supplies = session.exec(stmt).all()
    return wine_supplies


@ROUTER.patch("/quantity", status_code=200)
def update_wine_supply_quantity(quantity_update: WineSupplyQuantityUpdate) -> str:
    bottle_id = quantity_update.bottle_id
    new_quantity = quantity_update.new_quantity
    with Session(get_db_interface().engine) as session:
        supply = session.get(WineSupply, bottle_id)
        if not supply:
            raise HTTPException(status_code=404, detail=f"No supply found with id {bottle_id}")
        supply.quantity = new_quantity
        session.add(supply)
        session.commit()
    return "OK"


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
