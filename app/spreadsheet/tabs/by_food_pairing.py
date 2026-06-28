""" Tab to organize wines by food pairing """
from typing import Dict, List

from app.db.database import WineSupply


def generate_by_food_pairing_tab(wine_supplies: List[WineSupply]) -> List[dict]:
    """ Generate the 'By Food Pairing' tab of the spreadsheet """
    # Create a mapping of food pairings to wines
    pairing_map: Dict[str, List[WineSupply]] = {}
    for wine in wine_supplies:
        if wine.physical_location and wine.physical_location.name == "Consumed":
            continue  # Skip consumed wines
        for pairing in wine.food_pairings:
            if pairing.name not in pairing_map:
                pairing_map[pairing.name] = []
            pairing_map[pairing.name].append(wine)

    # Sort pairing map by pairing name
    pairing_map = dict(sorted(pairing_map.items(), key=lambda item: item[0].lower()))
    for wines in pairing_map.values():
        wines.sort(key=lambda w: w.pct_alcohol.lower() if w.pct_alcohol else "0.0", reverse=True)

    # Create tab data structure
    tab_data = []
    for pairing_name, wines in pairing_map.items():
        tab_data.append({"Name": " "})  # Add a separator row
        tab_data.append({"Name": pairing_name})  # Add a header row for the food pairing
        for wine in wines:
            tab_data.append({
                "Name": wine.name,
                "Vineyard": wine.vendor if wine.vendor else "Unknown",
                "Vintage": wine.vintage,
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
                "Location": wine.physical_location.name if wine.physical_location else "Unknown",
                "Grapes": ", ".join([grape.name for grape in wine.grapes]) if wine.grapes else "Unknown",
                "Region": wine.region.name if wine.region else "Unknown",
                "Country": wine.country.name if wine.country else "Unknown",
                "PCT": wine.pct_alcohol if wine.pct_alcohol else "0.0",
                "Quantity": wine.quantity if wine.quantity else "1",
                "Obtainment Note": wine.obtainment_note if wine.obtainment_note else "",
                "Drink By Date": wine.drink_by_date if wine.drink_by_date else "Unknown",
                "Keywords": ", ".join([keyword.keyword for keyword in wine.keywords]) if wine.keywords else "n/a",
                "Tasting Notes": wine.tasting_notes if wine.tasting_notes else "",
            })

    return tab_data