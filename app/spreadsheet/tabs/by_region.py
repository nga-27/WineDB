""" Tab to organize wines by region """

def generate_by_region_tab(wine_supplies):
    """ Generate the 'By Region' tab of the spreadsheet """
    # Create a mapping of regions to wines
    region_map = {}
    for wine in wine_supplies:
        region_name = wine.region.name if wine.region else "Unknown"
        if region_name not in region_map:
            region_map[region_name] = []
        region_map[region_name].append(wine)

    # Create tab data structure
    tab_data = []
    for region_name, wines in region_map.items():
        for wine in wines:
            tab_data.append({
                "Region": region_name,
                "Name": wine.name,
                "Quantity": wine.quantity,
                "Vintage": wine.vintage,
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
                "Location": wine.physical_location.name if wine.physical_location else "Unknown",
            })

    return tab_data