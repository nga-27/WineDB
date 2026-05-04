""" Tab to collect consumed wines """
from typing import List, Dict

from app.db.database import WineSupply


def generate_consumed_tab(supply_wines: List[WineSupply]) -> List[dict]:
    """ Generate the 'Consumed' tab of the spreadsheet """
    tab_data: List[dict] = []
    for wine in supply_wines:
        if wine.physical_location and wine.physical_location.name == "Consumed":
            tab_data.append({
                "Name": wine.name,
                "Grapes": ", ".join([grape.name for grape in wine.grapes]) if wine.grapes else "Unknown",
                "Vintage": wine.vintage,
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
                "Consumed Date": wine.drank_date if wine.drank_date else "Unknown",
                "Consumed Note": wine.drank_event_notes if wine.drank_event_notes else "N/A",
                "Region": wine.region.name if wine.region else "Unknown",
                "Country": wine.country.name if wine.country else "Unknown",
                "PCT": wine.pct_alcohol if wine.pct_alcohol else "Unknown",
                "Quantity": wine.quantity if wine.quantity else "Unknown",
                "Obtainment Note": wine.obtainment_note if wine.obtainment_note else "None",
                "Location": wine.physical_location.name if wine.physical_location else "Unknown",
                "Drink By Date": wine.drink_by_date if wine.drink_by_date else "Unknown",
                "Keywords": ", ".join([keyword.keyword for keyword in wine.keywords]) if wine.keywords else "n/a",
                "Tasting Notes": wine.tasting_notes if wine.tasting_notes else "None",
                "Food Pairings": ", ".join([pairing.name for pairing in wine.food_pairings]) \
                    if wine.food_pairings else "n/a",
            })

    return tab_data