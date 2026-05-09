""" Generate the SQLite table """
import json
import os

from sqlmodel import create_engine, SQLModel, Field, Relationship


SETTINGS_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "settings.json"
)


# Association table for many-to-many relationship
class SupplyKeywordsLink(SQLModel, table=True):
    supply_id: str = Field(default=None, foreign_key="winesupply.upc_vintage_sd_id", primary_key=True)
    keyword_id: str = Field(default=None, foreign_key="keywords.keyword_id", primary_key=True)


class SupplyGrapeLink(SQLModel, table=True):
    supply_id: str = Field(default=None, foreign_key="winesupply.upc_vintage_sd_id", primary_key=True)
    variety_id: str = Field(default=None, foreign_key="grapevariety.variety_id", primary_key=True)


class SupplyFoodPairingLink(SQLModel, table=True):
    supply_id: str = Field(default=None, foreign_key="winesupply.upc_vintage_sd_id", primary_key=True)
    pairing_id: str = Field(default=None, foreign_key="foodpairing.pairing_id", primary_key=True)

#############################################

class Country(SQLModel, table=True):
    country_id: str = Field(primary_key=True, default=None)
    name: str
    description: str | None = None
    regions: list["Region"] = Relationship(back_populates="country")
    wines: list["WineSupply"] = Relationship(back_populates="country")


class Region(SQLModel, table=True):
    region_id: str = Field(primary_key=True, default=None)
    name: str
    description: str | None = None
    country_id: str | None = Field(default=None, foreign_key="country.country_id")
    country: Country | None = Relationship(back_populates="regions")
    wines: list["WineSupply"] = Relationship(back_populates="region")
    grapes: list["GrapeVariety"] = Relationship(back_populates="region")


class PhysicalLocation(SQLModel, table=True):
    """ Includes: Cellar, Fridge, Drank, etc. """
    location_id: str = Field(primary_key=True, default=None)
    name: str
    description: str | None = None
    wines: list["WineSupply"] = Relationship(back_populates="physical_location")


class WineType(SQLModel, table=True):
    type_id: str = Field(primary_key=True, default=None)
    name: str
    description: str | None = None
    wines: list["WineSupply"] = Relationship(back_populates="wine_type")


class WineSupply(SQLModel, table=True):
    # upc + vintage + supply/drank: ex: 12345678912-2020-S, 12345678912-XXXX-D (no vintage known)
    upc_vintage_sd_id: str = Field(primary_key=True, default=None)
    name: str
    quantity: int
    upc_barcode_id: str | None = None
    vintage: str | None = None
    vendor: str | None = None
    region_id: str | None = Field(default=None, foreign_key="region.region_id")
    region: Region | None = Relationship(back_populates="wines")
    pct_alcohol: str | None = None
    drink_by_date: str | None = None
    tasting_notes: str | None = None
    obtainment_note: str | None = None
    other_notes: str | None = None
    physical_location_id: str | None = Field(default=None, foreign_key="physicallocation.location_id")
    physical_location: PhysicalLocation | None = Relationship(back_populates="wines")
    wine_type_id: str | None = Field(default=None, foreign_key="winetype.type_id")
    wine_type: WineType | None = Relationship(back_populates="wines")
    country_id: str | None = Field(default=None, foreign_key="country.country_id")
    country: Country | None = Relationship(back_populates="wines")
    drank_event_notes: str | None = None
    drank_date: str | None = None
    keywords: list["Keywords"] = Relationship(back_populates="wines", link_model=SupplyKeywordsLink)
    food_pairings: list["FoodPairing"] = Relationship(back_populates="wines", link_model=SupplyFoodPairingLink)
    grapes: list["GrapeVariety"] = Relationship(back_populates="wines", link_model=SupplyGrapeLink)


class GrapeVariety(SQLModel, table=True):
    variety_id: str = Field(primary_key=True, default=None)
    name: str
    description: str | None = None
    region_id: str | None = Field(default=None, foreign_key="region.region_id")
    region: Region | None = Relationship(back_populates="grapes")
    wines: list[WineSupply] = Relationship(back_populates="grapes", link_model=SupplyGrapeLink)

class FoodPairing(SQLModel, table=True):
    pairing_id: str = Field(primary_key=True, default=None)
    name: str
    description: str | None = None
    wines: list[WineSupply] = Relationship(back_populates="food_pairings", link_model=SupplyFoodPairingLink)


class Keywords(SQLModel, table=True):
    keyword_id: str = Field(primary_key=True, default=None)
    keyword: str
    description: str | None = None
    wines: list[WineSupply] = Relationship(back_populates="keywords", link_model=SupplyKeywordsLink)


class DBInterface:

    def __init__(self):
        self.__has_initialized = False
        self.sql_file_name = "wineDB.db"
        self.sql_url = f"sqlite:///{self.sql_file_name}"
        self.engine = create_engine(self.sql_url)
        # self.engine = create_engine(self.sql_url, echo=True)
        if not os.path.exists(SETTINGS_FILE_PATH):
            # Create the file to be filled out
            with open(SETTINGS_FILE_PATH, "w", encoding='utf-8') as file_x:
                json.dump({"sync_path": ""}, file_x)

    def create_db_and_tables(self):
        if self.__has_initialized:
            return
        SQLModel.metadata.create_all(self.engine)
        self.__has_initialized = True


DB_INTERFACE = DBInterface()

def get_db_interface() -> DBInterface:
    return DB_INTERFACE
