from typing import List
import uuid

from fastapi import APIRouter
from sqlmodel import Session

from app.db.database import get_db_interface, Keywords


ROUTER = APIRouter(
    prefix="/keywords"
)


@ROUTER.get("/", status_code=200)
def get_keywords() -> List[Keywords]:
    keywords: List[Keywords] = []
    with Session(get_db_interface().engine) as session:
        keywords = session.query(Keywords).all()
    return keywords


@ROUTER.post("/", status_code=201)
def create_keyword(keyword: Keywords) -> str:
    for key, value in vars(keyword).items():
        if key == "keyword_id":
            setattr(keyword, key, str(uuid.uuid4()))
        elif value is None or value == "string":
            setattr(keyword, key, None)
    with Session(get_db_interface().engine) as session:
        session.add(keyword)
        session.commit()
        session.refresh(keyword)
    return "OK"