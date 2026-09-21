""" Tab for organizing wines by optional drink by date """
from typing import List

from app.db.database import WineSupply


def generate_by_drink_by_date_tab(wine_supplies: List[WineSupply]) -> List[dict]:
    """ Generate the 'By Drink By Date' tab of the spreadsheet """
    # Filter wines that have a drink_by_date set
    wines_with_drink_by = [wine for wine in wine_supplies if wine.drink_by_date]

    # Sort wines by drink_by_date
    sorted_wines: List[WineSupply] = sorted(wines_with_drink_by, key=lambda x: x.drink_by_date)

    # Create tab data structure
    tab_data = []
    for wine in sorted_wines:
        if wine.physical_location and wine.physical_location.name == "Consumed":
            continue  # Skip consumed wines
        tab_data.append({
            "Drink By Date": wine.drink_by_date,
            "Name": wine.name,
            "Vineyard": wine.vendor if wine.vendor else "Unknown",
            "Quantity": wine.quantity if wine.quantity else "1",
            "Vintage": wine.vintage,
            "Location": wine.physical_location.name if wine.physical_location else "Unknown",
            "Type": wine.wine_type.name if wine.wine_type else "Unknown",
            "Grapes": ", ".join([grape.name for grape in wine.grapes]) if wine.grapes else "Unknown",
            "Region": wine.region.name if wine.region else "Unknown",
            "Country": wine.country.name if wine.country else "Unknown",
            "PCT": wine.pct_alcohol if wine.pct_alcohol else "0.0",
            "Obtainment Note": wine.obtainment_note if wine.obtainment_note else "",
            "Keywords": ", ".join([keyword.keyword for keyword in wine.keywords]) if wine.keywords else "n/a",
            "Tasting Notes": wine.tasting_notes if wine.tasting_notes else "",
            "Food Pairings": ", ".join([pairing.name for pairing in wine.food_pairings]) \
                    if wine.food_pairings else "n/a",
        })

    return tab_data
