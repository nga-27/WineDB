""" Tab to organize wines by food pairing """

def generate_by_food_pairing_tab(wine_supplies):
    """ Generate the 'By Food Pairing' tab of the spreadsheet """
    # Create a mapping of food pairings to wines
    pairing_map = {}
    for wine in wine_supplies:
        for pairing in wine.food_pairings:
            if pairing.name not in pairing_map:
                pairing_map[pairing.name] = []
            pairing_map[pairing.name].append(wine)

    # Create tab data structure
    tab_data = []
    for pairing_name, wines in pairing_map.items():
        for wine in wines:
            tab_data.append({
                "Food Pairing": pairing_name,
                "Name": wine.name,
                "Quantity": wine.quantity,
                "Vintage": wine.vintage,
                "Type": wine.wine_type.name if wine.wine_type else "Unknown",
                "Location": wine.physical_location.name if wine.physical_location else "Unknown",
            })

    return tab_data