""" Tab to organize wines by region """
from typing import List, Dict
import logging

from app.db.database import WineSupply, Region
from app.logging_config import LOGGER_NAME


def generate_by_region_tab(wine_supplies: List[WineSupply],
                           regions: List[Region]) -> List[dict]:
    """ Generate the 'By Region' tab of the spreadsheet """
    # Create a mapping of regions to wines
    region_map: Dict[str, List[WineSupply]] = {}
    for wine in wine_supplies:
        if wine.physical_location and wine.physical_location.name == "Consumed":
            continue  # Skip consumed wines
        region_name = wine.region.name if wine.region else "Unknown"
        if region_name not in region_map:
            region = next((r for r in regions if r.name == region_name), None)
            description = region.description if region else "No description available."
            region_map[region_name] = {
                "wines": [],
                "description": description}
        region_map[region_name]["wines"].append(wine)

    # Sort region map by region name
    region_map = dict(sorted(region_map.items(), key=lambda item: item[0].lower()))

    # Create tab data structure
    tab_data: List[dict] = []
    for region_name, region_data in region_map.items():
        tab_data.append({"Name": " "})  # Add a separator row
        tab_data.append({"Name": region_name, "Type": region_data["description"]})  # Add a header row for the region
        for wine in region_data["wines"]:
            tab_data.append({
                "Name": wine.name,
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
                "Quantity": wine.quantity if wine.quantity else "1",
                "Location": wine.physical_location.name if wine.physical_location else "Unknown",
                "Vineyard": wine.vendor if wine.vendor else "Unknown",
                "Vintage": wine.vintage,
                "Grapes": ", ".join([grape.name for grape in wine.grapes]) if wine.grapes else "Unknown",
                "Country": wine.country.name if wine.country else "Unknown",
                "PCT": wine.pct_alcohol if wine.pct_alcohol else "0.0",
                "Obtainment Note": wine.obtainment_note if wine.obtainment_note else "",
                "Drink By Date": wine.drink_by_date if wine.drink_by_date else "Unknown",
                "Keywords": ", ".join([keyword.keyword for keyword in wine.keywords]) if wine.keywords else "n/a",
                "Tasting Notes": wine.tasting_notes if wine.tasting_notes else "",
                "Food Pairings": ", ".join([pairing.name for pairing in wine.food_pairings]) \
                    if wine.food_pairings else "n/a",
            })

    return tab_data