""" Location-related API utility functions for the cmd_app """
from typing import List, Tuple

import requests


def search_wine_locations_for_content(name: str | None = None) -> List[str]:
    """ Placeholder function to search for content based on user input """
    if name is None:
        results = requests.get("http://localhost:8282/locations", timeout=5)
    else:
        results = requests.get(f"http://localhost:8282/locations?name={name}", timeout=5)
    result_names = [f'{result["name"]}, id: {result["location_id"]}' for result in results.json()]
    result_names.sort()
    return result_names


def create_wine_location(name: str, description: str | None) -> Tuple[str, bool]:
    """ Placeholder function to create a new wine location entry based on user input """
    response = requests.post(
        "http://localhost:8282/locations/",
        json={"name": name, "description": description}, timeout=5)
    if response.status_code == 201:
        return response.json(), True
    return response.text, False
