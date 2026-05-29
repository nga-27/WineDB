from typing import List, Tuple, Union

import requests


def search_regions_for_content(name: str) -> List[str]:
    """ Placeholder function to search for content based on user input """
    results = requests.get(f"http://localhost:8282/regions?name={name}")
    result_names = [f'{result["name"]}, id: {result["region_id"]}' for result in results.json()]
    result_names.sort()
    return result_names


def create_region(name: str, country_id: str | None, description: str | None) -> Tuple[str, bool]:
    """ Placeholder function to create a new region entry based on user input """
    response = requests.post(
        "http://localhost:8282/regions/",
        json={"name": name, "country_id": country_id, "description": description})
    if response.status_code == 201:
        return response.json(), True
    else:
        return response.text, False


def get_country_from_region(region_id: str) -> Tuple[Union[str, None], Union[str, None]]:
    """ Gets the country name for a given region ID, or None if there is no linked country """
    response = requests.get(f"http://localhost:8282/regions/{region_id}")
    if response.status_code != 200:
        return None, None
    region_data = response.json()
    country_id = region_data.get("country_id")
    if country_id is None:
        return None, None
    country_response = requests.get(f"http://localhost:8282/countries/{country_id}")
    if country_response.status_code != 200:
        return None, None
    country_data = country_response.json()
    return country_data.get("name"), country_id
