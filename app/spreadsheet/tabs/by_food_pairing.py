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

    # Create tab data structure
    tab_data = []
    for pairing_name, wines in pairing_map.items():
        for wine in wines:
            tab_data.append({
                "Food Pairing": pairing_name,
                "Name": wine.name,
                "Quantity": wine.quantity,
                "Vintage": wine.vintage,
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
                "Location": wine.physical_location.name if wine.physical_location else "Unknown",
            })

    return tab_data