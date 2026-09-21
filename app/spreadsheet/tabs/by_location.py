""" Tab to organize wines by region """
from typing import List, Dict

from app.db.database import WineSupply, PhysicalLocation


def generate_by_location_tab(wine_supplies: List[WineSupply],
                             locations: List[PhysicalLocation]) -> List[dict]:
    """ Generate the 'By Location' tab of the spreadsheet """
    # Create a mapping of locations to wines
    location_map: Dict[str, List[WineSupply]] = {}
    for wine in wine_supplies:
        if wine.physical_location and wine.physical_location.name == "Consumed":
            continue  # Skip consumed wines
        location_name = wine.physical_location.name if wine.physical_location else "Unknown"
        if location_name not in location_map:
            location = next((l for l in locations if l.name == location_name), None)
            description = location.description if location else "No description available."
            location_map[location_name] = {
                "wines": [],
                "description": description}
        location_map[location_name]["wines"].append(wine)

    # Sort location map by location name
    location_map = dict(sorted(location_map.items(), key=lambda item: item[0].lower()))
    for wines in location_map.values():
        wines["wines"].sort(key=lambda w: w.pct_alcohol.lower() if w.pct_alcohol else "0.0", reverse=True)

    # Create tab data structure
    tab_data: List[dict] = []
    for location_name, location_data in location_map.items():
        tab_data.append({"Name": " "})  # Add a separator row
        tab_data.append({"Name": location_name, "Vineyard": location_data["description"]})  # Add a header row for the location
        for wine in location_data["wines"]:
            tab_data.append({
                "Name": wine.name,
                "Vineyard": wine.vendor if wine.vendor else "Unknown",
                "Vintage": wine.vintage,
                "Quantity": wine.quantity if wine.quantity else "Unknown",
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
                "Grapes": ", ".join([grape.name for grape in wine.grapes]) if wine.grapes else "Unknown",
                "Country": wine.country.name if wine.country else "Unknown",
                "PCT": wine.pct_alcohol if wine.pct_alcohol else "0.0",
                "Obtainment Note": wine.obtainment_note if wine.obtainment_note else "",
                "Region": wine.region.name if wine.region else "Unknown",
                "Drink By Date": wine.drink_by_date if wine.drink_by_date else "Unknown",
                "Keywords": ", ".join([keyword.keyword for keyword in wine.keywords]) if wine.keywords else "n/a",
                "Tasting Notes": wine.tasting_notes if wine.tasting_notes else "",
                "Food Pairings": ", ".join([pairing.name for pairing in wine.food_pairings]) \
                    if wine.food_pairings else "n/a",
            })

    return tab_data