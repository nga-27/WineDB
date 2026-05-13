""" Tab to organize wines by keywords """

from typing import List, Dict

from app.db.database import WineSupply


def generate_by_keyword_tab(wine_supplies: List[WineSupply]) -> List[dict]:
    """ Generate the 'By Keyword' tab of the spreadsheet """
    # Create a mapping of keywords to wines
    keyword_map: Dict[str, List[WineSupply]] = {}
    for wine in wine_supplies:
        if wine.physical_location and wine.physical_location.name == "Consumed":
            continue  # Skip consumed wines
        for keyword in wine.keywords:
            if keyword.keyword not in keyword_map:
                keyword_map[keyword.keyword] = []
            keyword_map[keyword.keyword].append(wine)

    # Sort keyword map by keyword name
    keyword_map = dict(sorted(keyword_map.items(), key=lambda item: item[0].lower()))

    # Create tab data structure
    tab_data: List[dict] = []
    for keyword_name, wines in keyword_map.items():
        tab_data.append({"Name": " "})  # Add a separator row
        tab_data.append({"Name": keyword_name})  # Add a header row for the keyword
        for wine in wines:
            tab_data.append({
                "Name": wine.name,
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
                "Grapes": ", ".join([grape.name for grape in wine.grapes]) if wine.grapes else "Unknown",
                "Vintage": wine.vintage,
                "Region": wine.region.name if wine.region else "Unknown",
                "Country": wine.country.name if wine.country else "Unknown",
                "PCT": wine.pct_alcohol if wine.pct_alcohol else "Unknown",
                "Quantity": wine.quantity if wine.quantity else "Unknown",
                "Obtainment Note": wine.obtainment_note if wine.obtainment_note else "None",
                "Location": wine.physical_location.name if wine.physical_location else "Unknown",
                "Drink By Date": wine.drink_by_date if wine.drink_by_date else "Unknown",
                "Tasting Notes": wine.tasting_notes if wine.tasting_notes else "None",
                "Food Pairings": ", ".join([pairing.name for pairing in wine.food_pairings]) \
                    if wine.food_pairings else "n/a",
            })

    return tab_data


def generate_keyword_summary(wine_supplies: List[WineSupply]) -> List[dict]:
    """ Generate a summary of keyword usage across wines """
    summary = {}
    for wine in wine_supplies:
        if wine.physical_location and wine.physical_location.name == "Consumed":
            continue  # Skip consumed wines
        for keyword in wine.keywords:
            if keyword.keyword not in summary:
                summary[keyword.keyword] = 0
            summary[keyword.keyword] += 1
    
    # Create tab data structure
    tab_data: List[dict] = []
    for keyword_name, count in summary.items():
        tab_data.append({
            "Keyword": keyword_name,
            "Count": count
        })

    return tab_data
