""" Grape variety-related API utility functions for the cmd_app """
from typing import List, Tuple

import requests


def search_wine_grapes_for_content(name: str) -> List[str]:
    """ Placeholder function to search for content based on user input """
    results = requests.get(f"http://localhost:8282/grape_varieties?name={name}", timeout=5)
    result_names = [f'{result["name"]}, id: {result["variety_id"]}' for result in results.json()]
    result_names.sort()
    return result_names


def create_wine_grape(
        name: str, description: str | None, region_id: str | None) -> Tuple[str, bool]:
    """ Placeholder function to create a new wine grape entry based on user input """
    response = requests.post(
        "http://localhost:8282/grape_varieties/",
        json={"name": name, "description": description, "region_id": region_id}, timeout=5)
    if response.status_code == 201:
        return response.json(), True
    return response.text, False
