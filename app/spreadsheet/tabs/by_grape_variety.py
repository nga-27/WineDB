""" Tab to organize wines by grape variety """

def generate_by_grape_variety_tab(wine_supplies):
    """ Generate the 'By Grape Variety' tab of the spreadsheet """
    # Create a mapping of grape varieties to wines
    variety_map = {}
    for wine in wine_supplies:
        for variety in wine.grape_varieties:
            if variety.name not in variety_map:
                variety_map[variety.name] = []
            variety_map[variety.name].append(wine)

    # Create tab data structure
    tab_data = []
    for variety_name, wines in variety_map.items():
        for wine in wines:
            tab_data.append({
                "Grape Variety": variety_name,
                "Name": wine.name,
                "Quantity": wine.quantity,
                "Vintage": wine.vintage,
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
                "Location": wine.physical_location.name if wine.physical_location else "Unknown",
            })

    return tab_data