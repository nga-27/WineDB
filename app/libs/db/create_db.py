""" Generate the SQLite table """
from sqlmodel import create_engine, SQLModel, Field


class WineSupply(SQLModel, table=True):
    upc_id: str = Field(primary_key=True)
    name: str
    location: str
    quantity: int
    wine_type: str | None = None
    vintage: str | None = None
    vendor: str | None = None
    pct_alcohol: str | None = None
    food_pair: str | None = None
    grapes: str | None = None
    drink_by: str | None = None
    tasting_notes: str | None = None
    obtainment_note: str | None = None
    other_notes: str | None = None


class WineDrank(SQLModel, table=True):
    upc_id: str = Field(primary_key=True)
    name: str
    location: str
    quantity: int
    drank_dates: str
    drank_event_notes: str | None = None
    rating: str | None = None
    wine_type: str | None = None
    vintage: str | None = None
    vendor: str | None = None
    pct_alcohol: str | None = None
    food_pair: str | None = None
    grapes: str | None = None
    drink_by: str | None = None
    tasting_notes: str | None = None
    obtainment_note: str | None = None
    other_notes: str | None = None


class DBInterface:

    def __init__(self):
        self.__has_initialized = False
        self.sql_file_name = "wineDB.db"
        self.sql_url = f"sqlite:///{self.sql_file_name}"
        self.engine = create_engine(self.sql_url, echo=True)

    def create_db_and_tables(self):
        if self.__has_initialized:
            return
        print("creating DB...")
        SQLModel.metadata.create_all(self.engine)
        self.__has_initialized = True


DB_INTERFACE = DBInterface()

def get_db_interface() -> DBInterface:
    return DB_INTERFACE
