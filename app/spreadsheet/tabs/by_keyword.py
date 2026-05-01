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

    # Create tab data structure
    tab_data: List[dict] = []
    for keyword_name, wines in keyword_map.items():
        for wine in wines:
            tab_data.append({
                "Keyword": keyword_name,
                "Name": wine.name,
                "Quantity": wine.quantity,
                "Vintage": wine.vintage,
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
                "Location": wine.physical_location.name if wine.physical_location else "Unknown",
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
