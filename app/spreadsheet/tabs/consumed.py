""" Tab to collect consumed wines """
from typing import List, Tuple

from app.db.database import WineSupply


def cleanup_tab_data(wine: WineSupply) -> Tuple[List[str], List[str]]:
    """ Clean up the data for the 'Consumed' tab of the spreadsheet """
    drink_date = wine.drank_date if wine.drank_date else "Unknown"
    if drink_date != "Unknown":
        # If there are multiple dates, we want to show them all, separated by commas
        drink_date_list = [d.strip() for d in drink_date.split(";") if len(d.strip()) > 0]
        if len(drink_date_list) > 5:
            length = len(drink_date_list) - 5
            drink_date_list = [drink_date_list[0]] + drink_date_list[-4:] + \
                [f"... and {length} more"]
        drink_date = "; ".join(drink_date_list)
    drink_event_notes = wine.drank_event_notes if wine.drank_event_notes else "Unknown"
    if drink_event_notes != "Unknown":
        drink_event_notes_list = [
            n.strip() for n in drink_event_notes.split(";") if len(n.strip()) > 0]
        if len(drink_event_notes_list) > 5:
            length = len(drink_event_notes_list) - 5
            drink_event_notes_list = [drink_event_notes_list[0]] + \
                drink_event_notes_list[-4:] + [f"... and {length} more"]
        drink_event_notes = "; ".join(drink_event_notes_list)
    drink_rating_notes = wine.drank_rating_notes if wine.drank_rating_notes else "Unknown"
    if drink_rating_notes != "Unknown":
        drink_rating_notes_list = [
            n.strip() for n in drink_rating_notes.split(";") if len(n.strip()) > 0]
        if len(drink_rating_notes_list) > 5:
            length = len(drink_rating_notes_list) - 5
            drink_rating_notes_list = [drink_rating_notes_list[0]] + \
                drink_rating_notes_list[-4:] + [f"... and {length} more"]
        drink_rating_notes = "; ".join(drink_rating_notes_list)
    return drink_date, drink_event_notes, drink_rating_notes


def generate_consumed_tab(supply_wines: List[WineSupply]) -> List[dict]:
    """ Generate the 'Consumed' tab of the spreadsheet """
    tab_data: List[dict] = []
    for wine in supply_wines:
        if wine.physical_location and wine.physical_location.name == "Consumed":
            drink_date, drink_event_notes, drink_rating_notes = cleanup_tab_data(wine)
            tab_data.append({
                "Name": wine.name,
                "Vineyard": wine.vendor if wine.vendor else "Unknown",
                "Vintage": wine.vintage,
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
                "Quantity": wine.quantity if wine.quantity else "Unknown",
                "Rating": wine.drank_rating if wine.drank_rating else "n/a",
                "Rating Notes": drink_rating_notes,
                "Consumed Date(s)": drink_date,
                "Consumed Note": drink_event_notes,
                "Grapes": ", ".join([grape.name for grape in wine.grapes]) \
                    if wine.grapes else "Unknown",
                "Region": wine.region.name if wine.region else "Unknown",
                "Country": wine.country.name if wine.country else "Unknown",
                "PCT": wine.pct_alcohol if wine.pct_alcohol else "Unknown",
                "Obtainment Note": wine.obtainment_note if wine.obtainment_note else "None",
                "Location": wine.physical_location.name if wine.physical_location else "Unknown",
                "Drink By Date": wine.drink_by_date if wine.drink_by_date else "Unknown",
                "Keywords": ", ".join([keyword.keyword for keyword in wine.keywords]) \
                    if wine.keywords else "n/a",
                "Tasting Notes": wine.tasting_notes if wine.tasting_notes else "None",
                "Food Pairings": ", ".join([pairing.name for pairing in wine.food_pairings]) \
                    if wine.food_pairings else "n/a",
            })

    tab_data.sort(key=lambda x: x["Rating"] if x["Rating"] != "n/a" else "0.0", reverse=True)
    return tab_data