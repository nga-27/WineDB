from typing import List
import uuid
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.logging_config import LOGGER_NAME
from app.db.database import get_db_interface, Keywords, SupplyKeywordsLink


class CreateKeywordRequest(BaseModel):
    keyword: str
    description: str | None = None


ROUTER = APIRouter(
    prefix="/keywords",
    tags=["keywords"]
)


@ROUTER.get("/", status_code=200)
def get_keywords(name: str | None = None, upc_vintage_sd_id: str | None = None) -> List[Keywords]:
    keywords: List[Keywords] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(Keywords)
        if name:
            stmt = stmt.where(Keywords.name.ilike(f"%{name}%"))
        if upc_vintage_sd_id:
            stmt = stmt.join(SupplyKeywordsLink, Keywords.keyword_id == SupplyKeywordsLink.keyword_id)
            stmt = stmt.where(SupplyKeywordsLink.supply_id == upc_vintage_sd_id)
        keywords = session.exec(stmt).all()
    return keywords


@ROUTER.post("/", status_code=201)
def create_keyword(keyword: CreateKeywordRequest) -> str:
    keywords: List[Keywords] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(Keywords)
        stmt = stmt.where(Keywords.keyword == keyword.keyword)
        keywords = session.exec(stmt).all()
    if len(keywords) > 0:
        return keywords[0].keyword_id

    keyword_obj = Keywords(
        keyword_id=str(uuid.uuid4()),
        keyword=keyword.keyword,
        description=keyword.description
    )
    try:
        with Session(get_db_interface().engine) as session:
            session.add(keyword_obj)
            session.commit()
            session.refresh(keyword_obj)
    except Exception as exc:
        logger = logging.getLogger(LOGGER_NAME)
        logger.error(f"Error creating keyword entry: {exc}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the keyword entry.")
    return keyword_obj.keyword_id
