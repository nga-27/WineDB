""" Wine type-related API utility functions for the cmd_app """
from typing import List, Tuple

import requests


def search_wine_types_for_content(name: str) -> List[str]:
    """ Placeholder function to search for content based on user input """
    results = requests.get(f"http://localhost:8282/wine_types?name={name}", timeout=5)
    result_names = [f'{result["name"]}, id: {result["type_id"]}' for result in results.json()]
    return result_names


def create_wine_type(name: str, description: str | None) -> Tuple[str, bool]:
    """ Placeholder function to create a new wine type entry based on user input """
    response = requests.post(
        "http://localhost:8282/wine_types/",
        json={"name": name, "description": description}, timeout=5)
    if response.status_code == 201:
        return response.json(), True
    return response.text, False
