""" Tab to organize wines by alcohol content (Red, White, etc.) """
from typing import Dict, List

from app.db.database import WineSupply


def generate_wine_by_pct(wine_supplies: List[WineSupply]) -> List[dict]:
    """ Generate the 'By Type' tab of the spreadsheet """
    # Create a mapping of wine types to wines
    wines_to_display: List[WineSupply] = []
    for wine in wine_supplies:
        if wine.physical_location and wine.physical_location.name in ("Consumed", "Fridge"):
            continue  # Skip consumed wines
        wines_to_display.append(wine)

    for wine in wines_to_display:
        if not wine.pct_alcohol:
            wine.pct_alcohol = "0.0"
        else:
            try:
                wine.pct_alcohol = str(float(wine.pct_alcohol))
            except ValueError:
                wine.pct_alcohol = "0.0"
    wines_to_display.sort(
        key=lambda w: float(w.pct_alcohol) if w.pct_alcohol else 0.0, reverse=True)

    # Create tab data structure
    tab_data: List[dict] = []
    for wine in wines_to_display:
        tab_data.append({
            "PCT": wine.pct_alcohol if wine.pct_alcohol else "0.0",
            "Name": wine.name,
            "Vineyard": wine.vendor if wine.vendor else "Unknown",
            "Type": wine.wine_type.name if wine.wine_type else "Unknown",
            "Grapes": ", ".join([grape.name for grape in wine.grapes]) if wine.grapes else "Unknown",
            "Vintage": wine.vintage,
            "Region": wine.region.name if wine.region else "Unknown",
            "Country": wine.country.name if wine.country else "Unknown",
            "Quantity": wine.quantity if wine.quantity else "Unknown",
            "Obtainment Note": wine.obtainment_note if wine.obtainment_note else "",
            "Location": wine.physical_location.name if wine.physical_location else "Unknown",
            "Drink By Date": wine.drink_by_date if wine.drink_by_date else "Unknown",
            "Keywords": ", ".join([keyword.keyword for keyword in wine.keywords]) if wine.keywords else "n/a",
            "Tasting Notes": wine.tasting_notes if wine.tasting_notes else "",
            "Food Pairings": ", ".join([pairing.name for pairing in wine.food_pairings]) \
                if wine.food_pairings else "n/a",
        })

    return tab_data
