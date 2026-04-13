from typing import List
import uuid

from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import Session, select

from app.db.database import get_db_interface, Keywords


class CreateKeywordRequest(BaseModel):
    keyword: str
    description: str | None = None


ROUTER = APIRouter(
    prefix="/keywords",
    tags=["keywords"]
)


@ROUTER.get("/", status_code=200)
def get_keywords(name: str | None = None) -> List[Keywords]:
    keywords: List[Keywords] = []
    with Session(get_db_interface().engine) as session:
        stmt = select(Keywords)
        if name:
            stmt = stmt.where(Keywords.name.ilike(f"%{name}%"))
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
    with Session(get_db_interface().engine) as session:
        session.add(keyword_obj)
        session.commit()
        session.refresh(keyword_obj)
    return keyword_obj.keyword_id
