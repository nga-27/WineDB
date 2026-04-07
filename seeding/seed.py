""" Create a script to seed the DB via API calls to the backend """
import sys
import os
import time
import subprocess
import requests

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Set PYTHONPATH for subprocess
env = os.environ.copy()
env['PYTHONPATH'] = project_root

from app.db.database import get_db_interface


def seed_database():
    # Create database tables
    db_interface = get_db_interface()
    db_interface.create_db_and_tables()

    # Start the API server
    process = subprocess.Popen(
        ["uvicorn", "app.app:app", "--log-level=warning", "--port=8282"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for the server to start
    time.sleep(3)  # Adjust if needed

    base_url = "http://localhost:8282"

    # Check if server is up
    try:
        response = requests.get(f"{base_url}/start")
        if response.status_code != 200:
            print("Server not ready")
            return
    except requests.exceptions.RequestException:
        print("Failed to connect to server")
        return

    # Sample data for countries
    countries = [
        {"name": "France", "description": "Famous for Bordeaux, Burgundy, and Champagne regions."},
        {"name": "Italy", "description": "Known for Tuscany, Piedmont, and Veneto wine regions."},
        {"name": "Spain", "description": "Home to Rioja, Ribera del Duero, and Priorat."},
        {"name": "United States", "description": "California's Napa Valley and Sonoma are prominent."},
        {"name": "Argentina", "description": "Mendoza is a key wine-producing region."},
        {"name": "Australia", "description": "Barossa Valley and Margaret River are notable."},
        {"name": "Chile", "description": "Maipo Valley and Casablanca Valley."},
        {"name": "Germany", "description": "Mosel and Rheingau regions."},
        {"name": "Portugal", "description": "Douro Valley for Port wine."},
        {"name": "New Zealand", "description": "Marlborough for Sauvignon Blanc."}
    ]

    # Seed countries
    for country in countries:
        response = requests.post(f"{base_url}/countries/", json=country)
        print(f"Created country {country['name']}: {response.status_code}")

    # Sample data for wine types
    wine_types = [
        {"name": "Red", "description": "Full-bodied wines from dark grapes."},
        {"name": "White", "description": "Light wines from green or yellow grapes."},
        {"name": "Rosé", "description": "Pink wines from red grape skins."},
        {"name": "Sparkling", "description": "Effervescent wines with bubbles."},
        {"name": "Dessert", "description": "Sweet wines often served with dessert."},
        {"name": "Fortified", "description": "Wines with added alcohol, like Port."}
    ]

    # Seed wine types
    for wine_type in wine_types:
        response = requests.post(f"{base_url}/wine_types/", json=wine_type)
        print(f"Created wine type {wine_type['name']}: {response.status_code}")

    # Sample data for grape varieties
    grape_varieties = [
        {"name": "Cabernet Sauvignon", "description": "Bold red grape, often blended.", "region": "Bordeaux"},
        {"name": "Chardonnay", "description": "Versatile white grape.", "region": "Burgundy"},
        {"name": "Pinot Noir", "description": "Light red grape, finicky to grow.", "region": "Burgundy"},
        {"name": "Merlot", "description": "Soft red grape.", "region": "Bordeaux"},
        {"name": "Sauvignon Blanc", "description": "Crisp white grape.", "region": "Loire"},
        {"name": "Syrah", "description": "Spicy red grape.", "region": "Rhône"},
        {"name": "Riesling", "description": "Aromatic white grape.", "region": "Mosel"},
        {"name": "Malbec", "description": "Bold red grape.", "region": "Mendoza"},
        {"name": "Sangiovese", "description": "Italian red grape.", "region": "Tuscany"},
        {"name": "Tempranillo", "description": "Spanish red grape.", "region": "Rioja"}
    ]

    # Seed grape varieties
    for grape in grape_varieties:
        response = requests.post(f"{base_url}/grape_varieties/", json=grape)
        print(f"Created grape variety {grape['name']}: {response.status_code}")

    # Sample data for locations
    locations = [
        {"name": "Cellar", "description": "Long-term storage in a cool, dark place."},
        {"name": "Fridge", "description": "Short-term storage for immediate consumption."},
        {"name": "Consumed", "description": "Wines that have been drunk."}
    ]

    # Seed locations
    for location in locations:
        response = requests.post(f"{base_url}/locations/", json=location)
        print(f"Created location {location['name']}: {response.status_code}")

    # Fetch created IDs for relationships
    def map_by_name(endpoint, id_key="location_id"):
        response = requests.get(f"{base_url}/{endpoint}/")
        response.raise_for_status()
        return {item["name"]: item[id_key] for item in response.json()}

    location_ids = map_by_name("locations", id_key="location_id")
    wine_type_ids = map_by_name("wine_types", id_key="type_id")
    country_ids = map_by_name("countries", id_key="country_id")
    grape_varieties = requests.get(f"{base_url}/grape_varieties/").json()
    grape_ids = {item["name"]: item["variety_id"] for item in grape_varieties}

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
        print(f"Created keyword {keyword['keyword']}: {response.status_code}")

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
        print(f"Created food pairing {pairing['name']}: {response.status_code}")

    food_pairings_list = requests.get(f"{base_url}/food_pairings/").json()
    pairing_ids = {item["name"]: item["pairing_id"] for item in food_pairings_list}

    # Sample data for wine supplies
    wine_supplies = [
        {
            "name": "Chateau Montrose",
            "quantity": 3,
            "vintage": "2015",
            "vendor": "Wine Merchant",
            "region": "Bordeaux",
            "pct_alcohol": "13.5%",
            "drink_by_date": "2035-12-31",
            "tasting_notes": "Black fruit, cedar, firm tannins.",
            "obtainment_note": "Purchased from local wine shop.",
            "other_notes": "Cellar for aging.",
            "physical_location_id": location_ids.get("Cellar"),
            "wine_type_id": wine_type_ids.get("Red"),
            "country_id": country_ids.get("France"),
            "grape_ids": [grape_ids["Cabernet Sauvignon"], grape_ids["Merlot"]],
            "food_pairing_ids": [pairing_ids["Red Meat"], pairing_ids["Cheese"]]
        },
        {
            "name": "Cloudy Bay Sauvignon Blanc",
            "quantity": 6,
            "vintage": "2022",
            "vendor": "Importer Co.",
            "region": "Marlborough",
            "pct_alcohol": "13.0%",
            "drink_by_date": "2026-08-01",
            "tasting_notes": "Citrus, green apple, crisp acidity.",
            "obtainment_note": "Gifted by a friend.",
            "other_notes": "Serve chilled.",
            "physical_location_id": location_ids.get("Fridge"),
            "wine_type_id": wine_type_ids.get("White"),
            "country_id": country_ids.get("New Zealand"),
            "grape_ids": [grape_ids["Sauvignon Blanc"]],
            "food_pairing_ids": [pairing_ids["Fish"], pairing_ids["Poultry"]]
        },
        {
            "name": "Ridge Lytton Springs",
            "quantity": 2,
            "vintage": "2018",
            "vendor": "Direct from winery",
            "region": "Sonoma County",
            "pct_alcohol": "14.7%",
            "drink_by_date": "2030-11-01",
            "tasting_notes": "Dark berries, pepper, balanced acidity.",
            "obtainment_note": "Ordered online.",
            "other_notes": "Great with grilled meats.",
            "physical_location_id": location_ids.get("Cellar"),
            "wine_type_id": wine_type_ids.get("Red"),
            "country_id": country_ids.get("United States"),
            "grape_ids": [grape_ids["Syrah"]],
            "food_pairing_ids": [pairing_ids["Spicy Food"], pairing_ids["Red Meat"]]
        }
    ]

    # Seed wine supplies
    for wine_supply in wine_supplies:
        response = requests.post(f"{base_url}/wine_supplies/", json=wine_supply)
        print(f"Created wine supply {wine_supply['name']}: {response.status_code}")
        if response.status_code != 201:
            print(f"Failed to create wine supply {wine_supply['name']}: {response.text}")

    # Shutdown the server
    try:
        requests.get(f"{base_url}/shutdown")
    except:
        pass

    # Wait a bit and terminate the process if needed
    time.sleep(1)
    process.terminate()
    process.wait()

    print("Seeding complete.")


if __name__ == "__main__":
    seed_database()
