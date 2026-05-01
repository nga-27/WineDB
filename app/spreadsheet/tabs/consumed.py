""" Tab to collect consumed wines """
from typing import List, Dict

from app.db.database import WineSupply


def generate_consumed_tab(supply_wines: List[WineSupply]) -> List[dict]:
    """ Generate the 'Consumed' tab of the spreadsheet """
    tab_data: List[dict] = []
    for wine in supply_wines:
        if wine.physical_location == "Consumed":
            tab_data.append({
                "Name": wine.name,
                "Quantity": wine.quantity,
                "Vintage": wine.vintage,
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
            "Region": wine.region.name if wine.region else "Unknown",
            "Consumed Date": wine.consumed_date.strftime("%Y-%m-%d") if wine.consumed_date else "Unknown",
            "Location": wine.physical_location.name if wine.physical_location else "Unknown",
        })

    return tab_data