""" Utilities for API calls for bottles """
from typing import List, Tuple, Union
import logging

import requests

from app.logging_config import LOGGER_NAME
from .locations import search_wine_locations_for_content


def search_supply_for_content(name: str | None = None, vintage: str | None = None, omit_consumed: bool = True) -> List[str]:
    """ Placeholder function to search for content based on user input """
    consumed_location_id = "NOT-A-REAL-ID"
    if omit_consumed:
        consumed_location_id_list = search_wine_locations_for_content("Consumed")
        if len(consumed_location_id_list) > 0:
            consumed_location_id = consumed_location_id_list[0].split("id: ")[1]
    if name is None:
        results = requests.get(f"http://localhost:8282/wine_supplies")
        results_filtered = [result for result in results.json() if result["physical_location_id"] != consumed_location_id]
        result_names = [
            f'{result["name"]} ({result["vintage"]}) - {result["vendor"]} - QTY: {result["quantity"]}' \
                for result in results_filtered]
        return result_names
    if vintage:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}&vintage={vintage}")
    else:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}")
    results_filtered = [result for result in results.json() if result["physical_location_id"] != consumed_location_id]
    result_names = [f'{result["name"]} ({result["vintage"]})' for result in results_filtered]
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


def decrease_bottle_supply(name: str, vintage: str) -> Tuple[bool, Union[None, str]]:
    """ Placeholder function to decrease bottle supply based on user input """
    if vintage:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}&vintage={vintage}")
    else:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}")
    if len(results.json()) != 1:
        return False, f"Expected to find exactly one supply for {name} ({vintage}), but found {len(results.json())}."
    supply = results.json()[0]
    locations = search_wine_locations_for_content()
    consumed_id = [loc for loc in locations if "Consumed" in loc]
    if supply["physical_location_id"] == consumed_id:
        return False, f"Cannot consume {name} ({vintage}) because it is already marked as consumed."
    new_amount = supply["quantity"] - 1
    location_id = supply["physical_location_id"]
    if new_amount < 1:
        location_id = consumed_id
    bottle_id = supply["upc_vintage_sd_id"]
    response = requests.patch(
        f"http://localhost:8282/wine_supplies/quantity",
        json={"bottle_id": bottle_id, "new_quantity": new_amount, "physical_location_id": location_id})
    return response.status_code == 200, response.text


def create_bottle_entry(name: str, vintage: str | None = None, upc_barcode_id: str | None = None, vendor: str | None = None,
                        region: str | None = None, pct_alcohol: str | None = None, drink_by_date: str | None = None,
                        tasting_notes: str | None = None, obtainment_note: str | None = None, other_notes: str | None = None,
                        physical_location_id: str | None = None, wine_type_id: str | None = None, country_id: str | None = None,
                        grape_ids: List[str] | None = None, keyword_ids: List[str] | None = None, food_pairing_ids: List[str] | None = None,
                        quantity: int = 1) -> Tuple[bool, Union[None, str]]:
    """ Placeholder function to create a new bottle entry based on user input """
    logger = logging.getLogger(LOGGER_NAME)
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
        "country_id": country_id,
        "grape_ids": grape_ids,
        "physical_location_id": physical_location_id,
        "keyword_ids": keyword_ids,
        "food_pairing_ids": food_pairing_ids
    }
    logger.info(f"Creating bottle entry with payload: {payload}")
    try:
        response = requests.post(f"http://localhost:8282/wine_supplies", json=payload)
    except Exception as exc:
        logger.error(f"Error occurred while creating bottle entry: {exc}")
        return False, f"Error occurred while creating bottle entry: {exc}"
    logger.info(f"Create bottle entry response: {response.status_code} - {response.text}")
    return response.status_code == 201, response.text
