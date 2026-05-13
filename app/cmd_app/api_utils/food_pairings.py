from typing import List, Tuple

import requests


def search_food_pairings_for_content(name: str) -> List[str]:
    """ Placeholder function to search for content based on user input """
    results = requests.get(f"http://localhost:8282/food_pairings?name={name}")
    result_names = [f'{result["name"]}, id: {result["pairing_id"]}' for result in results.json()]
    result_names.sort()
    return result_names


def create_food_pairing(name: str, description: str | None) -> Tuple[str, bool]:
    """ Placeholder function to create a new food pairing entry based on user input """
    response = requests.post(
        "http://localhost:8282/food_pairings/",
        json={"name": name, "description": description})
    if response.status_code == 201:
        return response.json(), True
    else:
        return response.text, False
