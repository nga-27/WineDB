from typing import List, Tuple

import requests


def search_regions_for_content(name: str) -> List[str]:
    """ Placeholder function to search for content based on user input """
    results = requests.get(f"http://localhost:8282/regions?name={name}")
    result_names = [f'{result["name"]}, id: {result["region_id"]}' for result in results.json()]
    return result_names


def create_region(name: str, country_id: str | None, description: str | None) -> Tuple[str, bool]:
    """ Placeholder function to create a new region entry based on user input """
    response = requests.post(
        "http://localhost:8282/regions/",
        json={"name": name, "country_id": country_id, "description": description})
    if response.status_code == 201:
        return response.json()["region_id"], True
    else:
        return response.text, False
