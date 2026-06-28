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
    for wines in keyword_map.values():
        wines.sort(key=lambda w: w.pct_alcohol.lower() if w.pct_alcohol else "0.0", reverse=True)

    # Create tab data structure
    tab_data: List[dict] = []
    for keyword_name, wines in keyword_map.items():
        tab_data.append({"Name": " "})  # Add a separator row
        tab_data.append({"Name": keyword_name})  # Add a header row for the keyword
        for wine in wines:
            tab_data.append({
                "Name": wine.name,
                "Vineyard": wine.vendor if wine.vendor else "Unknown",
                "Vintage": wine.vintage,
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
                "Location": wine.physical_location.name if wine.physical_location else "Unknown",
                "Grapes": ", ".join([grape.name for grape in wine.grapes]) if wine.grapes else "Unknown",
                "Region": wine.region.name if wine.region else "Unknown",
                "Country": wine.country.name if wine.country else "Unknown",
                "PCT": wine.pct_alcohol if wine.pct_alcohol else "0.0",
                "Quantity": wine.quantity if wine.quantity else "1",
                "Obtainment Note": wine.obtainment_note if wine.obtainment_note else "",
                "Drink By Date": wine.drink_by_date if wine.drink_by_date else "Unknown",
                "Tasting Notes": wine.tasting_notes if wine.tasting_notes else "",
                "Food Pairings": ", ".join([pairing.name for pairing in wine.food_pairings]) \
                    if wine.food_pairings else "n/a",
            })

    return tab_data


def generate_keyword_summary(wine_supplies: List[WineSupply]) -> List[dict]:
    """ Generate a summary of keyword usage across wines """
    summary = {}
    total_available = 0
    total_consumed = 0
    for wine in wine_supplies:
        if wine.physical_location and wine.physical_location.name == "Consumed":
            total_consumed += wine.quantity if wine.quantity else 1
            continue  # Skip consumed wines
        total_available += wine.quantity if wine.quantity else 1
        for keyword in wine.keywords:
            if keyword.keyword not in summary:
                summary[keyword.keyword] = 0
            summary[keyword.keyword] += 1
    
    summary = dict(sorted(summary.items(), key=lambda item: item[1], reverse=True))
    # Create tab data structure
    tab_data: List[dict] = []
    for keyword_name, count in summary.items():
        tab_data.append({
            "Keyword": keyword_name,
            "Count": count,
            " ": "", # spacer
            "Total Bottles Available:": "",
            str(total_available): "",
            "Total Bottles Consumed:": "",
            str(total_consumed): "",
        })

    return tab_data
