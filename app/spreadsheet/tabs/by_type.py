""" Tab to organize wines by type (Red, White, etc.) """

def generate_by_type_tab(wine_supplies):
    """ Generate the 'By Type' tab of the spreadsheet """
    # Create a mapping of wine types to wines
    type_map = {}
    for wine in wine_supplies:
        type_name = wine.wine_type.name if wine.wine_type else "Unknown"
        if type_name not in type_map:
            type_map[type_name] = []
        type_map[type_name].append(wine)

    # Create tab data structure
    tab_data = []
    for type_name, wines in type_map.items():
        for wine in wines:
            tab_data.append({
                "Type": type_name,
                "Name": wine.name,
                "Quantity": wine.quantity,
                "Vintage": wine.vintage,
                "Region": wine.region.name if wine.region else "Unknown",
                "Location": wine.physical_location.name if wine.physical_location else "Unknown",
            })

    return tab_data