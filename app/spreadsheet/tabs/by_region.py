""" Tab to organize wines by region """
from typing import List, Dict

from app.db.database import WineSupply


def generate_by_region_tab(wine_supplies: List[WineSupply]) -> List[dict]:
    """ Generate the 'By Region' tab of the spreadsheet """
    # Create a mapping of regions to wines
    region_map: Dict[str, List[WineSupply]] = {}
    for wine in wine_supplies:
        if wine.physical_location and wine.physical_location.name == "Consumed":
            continue  # Skip consumed wines
        region_name = wine.region.name if wine.region else "Unknown"
        if region_name not in region_map:
            region_map[region_name] = []
        region_map[region_name].append(wine)

    # Create tab data structure
    tab_data: List[dict] = []
    for region_name, wines in region_map.items():
        tab_data.append({"Name": " "})  # Add a separator row
        tab_data.append({"Name": region_name})  # Add a header row for the region
        for wine in wines:
            tab_data.append({
                "Name": wine.name,
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
                "Grapes": ", ".join([grape.name for grape in wine.grapes]) if wine.grapes else "Unknown",
                "Vintage": wine.vintage,
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