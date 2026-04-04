""" Tab to organize wines by type (Red, White, etc.) """
from typing import Dict, List

from app.db.database import WineSupply


def generate_by_type_tab(wine_supplies: List[WineSupply]):
    """ Generate the 'By Type' tab of the spreadsheet """
    # Create a mapping of wine types to wines
    type_map: Dict[str, List[WineSupply]] = {}
    for wine in wine_supplies:
        type_name = wine.wine_type.name if wine.wine_type else "Unknown"
        if type_name not in type_map:
            type_map[type_name] = []
        type_map[type_name].append(wine)

    # Create tab data structure
    tab_data = []
    for type_name, wines in type_map.items():
        for wine in wines:
            tab_data.append({
                "Type": type_name,
                "Name": wine.name,
                "Grapes": ", ".join([grape.name for grape in wine.grapes]) if wine.grapes else "Unknown",
                "Vintage": wine.vintage,
                "Region": wine.region.name if wine.region else "Unknown",
                "Country": wine.country.name if wine.country else "Unknown",
                "PCT": wine.pct_alcohol if wine.pct_alcohol else "Unknown",
                "Quantity": wine.quantity if wine.quantity else "Unknown",
                "Obtainment Note": wine.obtainment_note if wine.obtainment_note else "None",
                "Location": wine.physical_location.name if wine.physical_location else "Unknown",
                "Tasting Notes": wine.tasting_notes if wine.tasting_notes else "None",
                "Food Pairings": ", ".join([pairing.name for pairing in wine.food_pairings]) \
                    if wine.food_pairings else "n/a",
                "Drink By Date": wine.drink_by_date if wine.drink_by_date else "Unknown",
            })

    return tab_data