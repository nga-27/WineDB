""" Tab to organize wines by grape variety """
from typing import Dict, List

from app.db.database import WineSupply, GrapeVariety


def generate_by_grape_variety_tab(wine_supplies: List[WineSupply],
                                  grapes: List[GrapeVariety]) -> List[dict]:
    """ Generate the 'By Grape Variety' tab of the spreadsheet """
    # Create a mapping of grape varieties to wines
    variety_map: Dict[str, List[WineSupply]] = {}
    for wine in wine_supplies:
        if wine.physical_location and wine.physical_location.name == "Consumed":
            continue  # Skip consumed wines
        for variety in wine.grapes:
            if variety.name not in variety_map:
                grape = next((g for g in grapes if g.name == variety.name), None)
                description = grape.description if grape else "No description available."
                variety_map[variety.name] = {"wines": [], "description": description}
            variety_map[variety.name]["wines"].append(wine)
    
    # Sort variety map by variety name
    variety_map = dict(sorted(variety_map.items(), key=lambda item: item[0].lower()))
    for wines in variety_map.values():
        wines["wines"].sort(key=lambda w: w.pct_alcohol.lower() if w.pct_alcohol else "0.0", reverse=True)

    # Create tab data structure
    tab_data: List[dict] = []
    for variety_name, obj_data in variety_map.items():
        tab_data.append({"Name": " "})  # Add a separator row
        tab_data.append({"Name": variety_name, "Vineyard": obj_data["description"]})  # Add a header row for the grape variety
        for wine in obj_data["wines"]:
            tab_data.append({
                "Name": wine.name,
                "Vineyard": wine.vendor if wine.vendor else "Unknown",
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
                "Vintage": wine.vintage,
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