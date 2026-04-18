from typing import List, Tuple

import requests


def search_keywords_for_content(name: str) -> List[str]:
    """ Placeholder function to search for content based on user input """
    results = requests.get(f"http://localhost:8282/keywords?name={name}")
    result_names = [f'{result["keyword"]}, id: {result["keyword_id"]}' for result in results.json()]
    return result_names


def create_keyword(name: str, description: str | None) -> Tuple[str, bool]:
    """ Placeholder function to create a new keyword entry based on user input """
    response = requests.post(
        "http://localhost:8282/keywords/",
        json={"name": name, "description": description})
    if response.status_code == 201:
        return response.json(), True
    else:
        return response.text, False
