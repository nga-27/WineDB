""" Utilities for API calls for bottles """
from typing import Any, List, Tuple, Union

import requests


def search_for_content(name: str, vintage: str | None = None) -> List[str]:
    """ Placeholder function to search for content based on user input """
    if vintage:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}&vintage={vintage}")
    else:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}")
    result_names = [f'{result["name"]} ({result["vintage"]})' for result in results.json()]
    return result_names


def increase_bottle_supply(name: str, vintage: str) -> Tuple[bool, Union[None, str]]:
    """ Placeholder function to increase bottle supply based on user input """
    if vintage:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}&vintage={vintage}")
    else:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}")
    if len(results.json()) != 1:
        return False, f"Expected to find exactly one supply for {name} ({vintage}), but found {len(results.json())}."
    supply = results.json()[0]
    bottle_id = supply["upc_vintage_sd_id"]
    response = requests.patch(
        f"http://localhost:8282/wine_supplies/quantity",
        json={"bottle_id": bottle_id, "new_quantity": supply["quantity"] + 1})
    return response.status_code == 200, response.text


def create_bottle_entry(name: str, vintage: str | None = None, upc_barcode_id: str | None = None, vendor: str | None = None,
                        region: str | None = None, pct_alcohol: str | None = None, drink_by_date: str | None = None,
                        tasting_notes: str | None = None, obtainment_note: str | None = None, other_notes: str | None = None,
                        physical_location_id: str | None = None, wine_type_id: str | None = None, country_id: str | None = None,
                        quantity: int = 1) -> Tuple[bool, Union[None, str]]:
    """ Placeholder function to create a new bottle entry based on user input """
    payload = {
        "name": name,
        "vintage": vintage,
        "upc_barcode_id": upc_barcode_id,
        "vendor": vendor,
        "quantity": quantity,
        "region": region,
        "pct_alcohol": pct_alcohol,
        "drink_by_date": drink_by_date,
        "tasting_notes": tasting_notes,
        "obtainment_note": obtainment_note,
        "other_notes": other_notes,
        "physical_location_id": physical_location_id,
        "wine_type_id": wine_type_id,
        "country_id": country_id
    }
    response = requests.post(f"http://localhost:8282/wine_supplies", json=payload)
    return response.status_code == 201, response.text
