""" Tab to collect consumed wines """
from typing import List, Dict

from app.db.database import WineSupply


def generate_consumed_tab(supply_wines: List[WineSupply]) -> List[dict]:
    """ Generate the 'Consumed' tab of the spreadsheet """
    tab_data: List[dict] = []
    for wine in supply_wines:
        if wine.physical_location and wine.physical_location.name == "Consumed":
            tab_data.append({
                "Name": wine.name,
                "Quantity": wine.quantity,
                "Vintage": wine.vintage,
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
                "Region": wine.region.name if wine.region else "Unknown",
                "Consumed Date": wine.drank_date if wine.drank_date else "Unknown",
                "Consumed Note": wine.drank_event_notes if wine.drank_event_notes else "N/A",
            })

    return tab_data