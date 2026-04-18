import time

import requests


def auto_seed() -> bool:
    """ Function to load an empty DB with some default data """
    base_url = "http://localhost:8282"

    # Check if server is up
    num_retries = 5
    was_successful = False
    for _ in range(num_retries):
        try:
            response = requests.get(f"{base_url}/")
            if response.status_code == 200:
                was_successful = True
                break
        except requests.exceptions.RequestException as _:
            pass
        time.sleep(2)
    if not was_successful:
        return False

    # Sample data for countries
    countries = []

    # Seed countries
    for country in countries:
        response = requests.post(f"{base_url}/countries/", json=country)

    wine_types = [
        {"name": "Sparkling", "description": "Effervescent wines with bubbles."},
        {"name": "White", "description": "Light wines from green or yellow grapes."},
        {"name": "Orange", "description": "White wines fermented with skin contact."},
        {"name": "Rosé", "description": "Pink wines from red grapes fermented without skin contact."},
        {"name": "Red", "description": "Full-bodied wines from dark grapes."},
        {"name": "Fortified", "description": "Wines with added alcohol, like Port / Sherry."},
        {"name": "Dessert", "description": "Sweet wines often served with dessert, not necessarily fortified."},
    ]

    # Seed wine types
    for wine_type in wine_types:
        response = requests.post(f"{base_url}/wine_types/", json=wine_type)

    # Sample data for regions
    regions = []

    # Seed regions
    for region in regions:
        response = requests.post(f"{base_url}/regions/", json=region)

    # Sample data for grape varieties
    grape_varieties = []

    # Seed grape varieties
    for grape in grape_varieties:
        response = requests.post(f"{base_url}/grape_varieties/", json=grape)

    # Sample data for locations
    locations = [
        {"name": "Cellar", "description": "Long-term storage in a cool, dark place."},
        {"name": "Fridge", "description": "Short-term storage for immediate consumption."},
        {"name": "Consumed", "description": "Wines that have been drunk (or given away)."}
    ]

    # Seed locations
    for location in locations:
        response = requests.post(f"{base_url}/locations/", json=location)

    # Sample data for keywords
    keywords = [
        {"keyword": "Bold", "description": "Strong, full-bodied flavors."},
        {"keyword": "Light", "description": "Delicate and subtle."},
        {"keyword": "Dry", "description": "Not sweet, low residual sugar."},
        {"keyword": "Sweet", "description": "High residual sugar."},
        {"keyword": "Tannic", "description": "Astringent from tannins."},
        {"keyword": "Fruity", "description": "Prominent fruit flavors."},
        {"keyword": "Earthy", "description": "Soil-like or mineral notes."},
        {"keyword": "Oaky", "description": "Influenced by oak aging."},
        {"keyword": "Crisp", "description": "Fresh and acidic."},
        {"keyword": "Smooth", "description": "Soft and velvety texture."}
    ]

    # Seed keywords
    for keyword in keywords:
        response = requests.post(f"{base_url}/keywords/", json=keyword)

    # Sample data for food pairings
    food_pairings = [
        {"name": "Red Meat", "description": "Steak, lamb, beef dishes."},
        {"name": "Poultry", "description": "Chicken, turkey."},
        {"name": "Fish", "description": "Salmon, tuna, white fish."},
        {"name": "Cheese", "description": "Hard and soft cheeses."},
        {"name": "Pasta", "description": "Italian dishes with tomato or cream sauces."},
        {"name": "Dessert", "description": "Sweet treats like chocolate or fruit."},
        {"name": "Vegetables", "description": "Grilled or roasted veggies."},
        {"name": "Spicy Food", "description": "Dishes with heat and spices."}
    ]

    # Seed food pairings
    for pairing in food_pairings:
        response = requests.post(f"{base_url}/food_pairings/", json=pairing)

    return True
