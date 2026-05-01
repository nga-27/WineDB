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
            "Name": wine.name,
            "Drink By Date": wine.drink_by_date,
            "Quantity": wine.quantity,
            "Vintage": wine.vintage,
            "Type": wine.wine_type.name if wine.wine_type else "Unknown",
            "Location": wine.physical_location.name if wine.physical_location else "Unknown",
        })

    return tab_data
