""" Tab to organize wines by keywords """

def generate_by_keyword_tab(wine_supplies):
    """ Generate the 'By Keyword' tab of the spreadsheet """
    # Create a mapping of keywords to wines
    keyword_map = {}
    for wine in wine_supplies:
        for keyword in wine.keywords:
            if keyword.name not in keyword_map:
                keyword_map[keyword.name] = []
            keyword_map[keyword.name].append(wine)

    # Create tab data structure
    tab_data = []
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


def generate_keyword_summary(wine_supplies):
    """ Generate a summary of keyword usage across wines """
    summary = {}
    for wine in wine_supplies:
        for keyword in wine.keywords:
            if keyword.name not in summary:
                summary[keyword.name] = 0
            summary[keyword.name] += 1
    return summary
