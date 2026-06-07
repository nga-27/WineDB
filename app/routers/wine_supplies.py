from typing import List
import uuid
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.logging_config import LOGGER_NAME
from app.db.database import (
    Keywords,
    get_db_interface,
    WineSupply,
    GrapeVariety,
    FoodPairing,
    GrapeVariety,
    PhysicalLocation,
)


class WineSupplyCreate(BaseModel):
    name: str
    quantity: int
    upc_vintage_sd_id: str | None = None
    upc_barcode_id: str | None = None
    vintage: str | None = None
    vendor: str | None = None
    region_id: str | None = None
    pct_alcohol: str | None = None
    drink_by_date: str | None = None
    tasting_notes: str | None = None
    obtainment_note: str | None = None
    other_notes: str | None = None
    physical_location_id: str | None = None
    wine_type_id: str | None = None
    country_id: str | None = None
    # Additional consumption fields
    drank_event_notes: str | None = None
    drank_date: str | None = None
    drank_rating: str | None = None
    drank_rating_notes: str | None = None
    drank_rating_raw: str | None = None
    grape_ids: list[str] = []
    food_pairing_ids: list[str] = []
    keyword_ids: list[str] = []


class WineSupplyQuantityUpdate(BaseModel):
    bottle_id: str
    new_quantity: int
    drank_event_notes: str | None = None
    drank_date: str | None = None
    drank_rating: str | None = None
    drank_rating_notes: str | None = None
    drank_rating_raw: str | None = None


ROUTER = APIRouter(
    prefix="/wine_supplies",
    tags=["wine_supplies"]
)


@ROUTER.get("/", status_code=200)
def get_wine_supplies(name: str | None = None, vintage: str | None = None,
                      by_barcode: bool = False) -> List[dict]:
    result: List[dict] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(WineSupply)
        if by_barcode and name:
            stmt = stmt.where(WineSupply.upc_barcode_id == name)
        else:
            if name:
                stmt = stmt.where(WineSupply.name.ilike(f"%{name}%"))
            if vintage:
                stmt = stmt.where(WineSupply.vintage == vintage)
        wine_supplies = session.exec(stmt).all()

        for supply in wine_supplies:
            # Build a safe dict excluding relationship objects, then add grape ids
            supply_dict = supply.model_dump(
                exclude={
                    "region", "country", "physical_location", "wine_type", "keywords",
                    "food_pairings", "grapes"},
                exclude_none=True)
            supply_dict["grape_ids"] = [g.variety_id for g in supply.grapes] \
                if supply.grapes else []
            supply_dict["food_pairing_ids"] = [fp.pairing_id for fp in supply.food_pairings] \
                if supply.food_pairings else []
            supply_dict["keyword_ids"] = [k.keyword_id for k in supply.keywords] \
                if supply.keywords else []
            result.append(supply_dict)
    return result


@ROUTER.get("/joined", status_code=200)
def get_wine_supplies_joined() -> List[dict]:
    """Get all wine supplies with all relationships eagerly loaded."""
    with Session(get_db_interface().engine) as session:
        stmt = (
            select(WineSupply)
            .options(
                selectinload(WineSupply.wine_type),
                selectinload(WineSupply.region),
                selectinload(WineSupply.country),
                selectinload(WineSupply.physical_location),
                selectinload(WineSupply.grapes),
                selectinload(WineSupply.food_pairings),
                selectinload(WineSupply.keywords),
            )
        )
        wines = session.exec(stmt).all()

    # Build response with only name fields from relationships
    result = []
    for wine in wines:
        result.append({
            "upc_vintage_sd_id": wine.upc_vintage_sd_id,
            "name": wine.name,
            "quantity": wine.quantity,
            "upc_barcode_id": wine.upc_barcode_id,
            "vintage": wine.vintage,
            "vendor": wine.vendor,
            "pct_alcohol": wine.pct_alcohol,
            "drink_by_date": wine.drink_by_date,
            "tasting_notes": wine.tasting_notes,
            "obtainment_note": wine.obtainment_note,
            "other_notes": wine.other_notes,
            "drank_event_notes": wine.drank_event_notes,
            "drank_date": wine.drank_date,
            "wine_type": wine.wine_type.name if wine.wine_type else None,
            "region": wine.region.name if wine.region else None,
            "country": wine.country.name if wine.country else None,
            "physical_location": wine.physical_location.name if wine.physical_location else None,
            "drank_rating": wine.drank_rating if wine.drank_rating else None,
            "drank_rating_notes": wine.drank_rating_notes if wine.drank_rating_notes else None,
            "grapes": [g.name for g in wine.grapes] if wine.grapes else [],
            "food_pairings": [fp.name for fp in wine.food_pairings] if wine.food_pairings else [],
            "keywords": [k.keyword for k in wine.keywords] if wine.keywords else [],
        })
    return result


@ROUTER.patch("/quantity", status_code=200)
def update_wine_supply_quantity(quantity_update: WineSupplyQuantityUpdate) -> str:
    bottle_id = quantity_update.bottle_id
    new_quantity = quantity_update.new_quantity
    new_rating = quantity_update.drank_rating
    new_rating_notes = quantity_update.drank_rating_notes
    new_rating_raw = quantity_update.drank_rating_raw
    new_event_notes = quantity_update.drank_event_notes
    new_drank_date = quantity_update.drank_date
    with Session(get_db_interface().engine) as session:
        supply = session.get(WineSupply, bottle_id)
        if not supply:
            raise HTTPException(status_code=404, detail=f"No supply found with id {bottle_id}")
        supply.quantity = new_quantity
        supply.drank_rating = new_rating
        supply.drank_rating_notes = new_rating_notes
        supply.drank_rating_raw = new_rating_raw
        supply.drank_event_notes = new_event_notes
        supply.drank_date = new_drank_date
        session.add(supply)
        session.commit()
    return "OK"


@ROUTER.patch("/move", status_code=200)
def move_wine_supply(bottle_id: str, new_location_id: str) -> str:
    with Session(get_db_interface().engine) as session:
        supply = session.get(WineSupply, bottle_id)
        if not supply:
            raise HTTPException(status_code=404, detail=f"No supply found with id {bottle_id}")
        new_location = session.get(PhysicalLocation, new_location_id)
        if not new_location:
            raise HTTPException(status_code=404, detail=f"No physical location found with id {new_location_id}")
        supply.physical_location = new_location
        session.add(supply)
        session.commit()
    return "OK"


@ROUTER.patch("/update_linked_grapes", status_code=200)
def update_linked_grapes(bottle_id: str, grape_ids: List[str]) -> str:
    with Session(get_db_interface().engine) as session:
        supply = session.get(WineSupply, bottle_id)
        if not supply:
            raise HTTPException(status_code=404, detail=f"No supply found with id {bottle_id}")
        # Load GrapeVariety rows matching the provided ids and replace relationships
        if grape_ids:
            grapes = list(set(grape_ids))  # Remove duplicates
            grapes = session.exec(select(GrapeVariety).where(GrapeVariety.variety_id.in_(grape_ids))).all()
        else:
            grapes = []
        supply.grapes = grapes
        session.add(supply)
        session.commit()
    return "OK"


@ROUTER.patch("/update_linked_food_pairings", status_code=200)
def update_linked_food_pairings(bottle_id: str, food_pairing_ids: List[str]) -> str:
    with Session(get_db_interface().engine) as session:
        supply = session.get(WineSupply, bottle_id)
        if not supply:
            raise HTTPException(status_code=404, detail=f"No supply found with id {bottle_id}")
        # Load FoodPairing rows matching the provided ids and replace relationships
        if food_pairing_ids:
            food_pairings = list(set(food_pairing_ids))  # Remove duplicates
            food_pairings = session.exec(select(FoodPairing).where(FoodPairing.pairing_id.in_(food_pairing_ids))).all()
        else:
            food_pairings = []
        supply.food_pairings = food_pairings
        session.add(supply)
        session.commit()
    return "OK"


@ROUTER.patch("/update_linked_keywords", status_code=200)
def update_linked_keywords(bottle_id: str, keyword_ids: List[str]) -> str:
    with Session(get_db_interface().engine) as session:
        supply = session.get(WineSupply, bottle_id)
        if not supply:
            raise HTTPException(status_code=404, detail=f"No supply found with id {bottle_id}")
        # Load Keywords rows matching the provided ids and replace relationships
        if keyword_ids:
            keywords = list(set(keyword_ids))  # Remove duplicates
            keywords = session.exec(select(Keywords).where(Keywords.keyword_id.in_(keyword_ids))).all()
        else:
            keywords = []
        supply.keywords = keywords
        session.add(supply)
        session.commit()
    return "OK"


@ROUTER.post("/", status_code=201)
def create_wine_supply(wine_supply: WineSupplyCreate) -> str:
    logger = logging.getLogger(LOGGER_NAME)
    if not wine_supply.upc_vintage_sd_id:
        wine_supply.upc_vintage_sd_id = str(uuid.uuid4())
    
    wine_supplies: List[WineSupply] = []
    try:
        with Session(get_db_interface().engine) as session:
            stmt = select(WineSupply)
            if wine_supply.name:
                stmt = stmt.where(WineSupply.name == wine_supply.name)
            if wine_supply.vintage:
                stmt = stmt.where(WineSupply.vintage == wine_supply.vintage)
            if wine_supply.physical_location_id:
                stmt = stmt.where(WineSupply.physical_location_id == wine_supply.physical_location_id)
            wine_supplies = session.exec(stmt).all()
    except Exception as exc:
        logger.error(f"Error occurred while fetching wine supplies: {exc}")
        raise HTTPException(status_code=500, detail=f"Error occurred while fetching wine supplies: {exc}")

    if len(wine_supplies) > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Supply with name '{wine_supply.name}', vintage '{wine_supply.vintage}', " + \
                f"and physical location '{wine_supply.physical_location_id}' already exists.")
    logger.info(f"Wine grapes: {wine_supply.grape_ids}")
    try:
        db_supply = WineSupply(
            upc_vintage_sd_id=wine_supply.upc_vintage_sd_id,
            name=wine_supply.name,
            quantity=wine_supply.quantity,
            upc_barcode_id=wine_supply.upc_barcode_id,
            vintage=wine_supply.vintage,
            vendor=wine_supply.vendor,
            region_id=wine_supply.region_id,
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
            drank_rating=wine_supply.drank_rating,
            drank_rating_notes=wine_supply.drank_rating_notes,
            drank_rating_raw=wine_supply.drank_rating_raw
        )
        logger.info(f"Created WineSupply object: {db_supply.__dict__}")
    except Exception as exc:
        logger.error(f"Error creating wine supply object: {exc}")
        raise HTTPException(status_code=500, detail=f"Error creating wine supply object: {exc}")

    try:
        with Session(get_db_interface().engine) as session:
            session.add(db_supply)
            
            db_supply.grapes = [
                session.get(GrapeVariety, grape_id) for grape_id in wine_supply.grape_ids if grape_id]
            db_supply.food_pairings = [
                session.get(FoodPairing, pairing_id) for pairing_id in wine_supply.food_pairing_ids if pairing_id]
            db_supply.keywords = [
                session.get(Keywords, keyword_id) for keyword_id in wine_supply.keyword_ids if keyword_id
            ]

            session.commit()
            session.refresh(db_supply)
    except Exception as exc:
        logger.error(f"Error creating wine supply: {exc}")
        raise HTTPException(status_code=500, detail=f"Error creating wine supply: {exc}")

    return "OK"


@ROUTER.delete("/{bottle_id}", status_code=200)
def delete_wine_supply(bottle_id: str) -> str:
    with Session(get_db_interface().engine) as session:
        supply = session.get(WineSupply, bottle_id)
        if not supply:
            raise HTTPException(status_code=404, detail=f"No supply found with id {bottle_id}")
        session.delete(supply)
        session.commit()
    return "OK"
