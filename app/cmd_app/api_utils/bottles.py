""" Utilities for API calls for bottles """
from typing import List, Tuple, Union
import logging
import time

import requests

from app.logging_config import LOGGER_NAME
from .locations import search_wine_locations_for_content


def search_supply_for_content(name: str | None = None, vintage: str | None = None,
                              omit_consumed: bool = True, by_barcode: bool = False) -> List[str]:
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
    if by_barcode:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}&by_barcode=true")
        results_filtered = [result for result in results.json() if result["physical_location_id"] != consumed_location_id]
        result_names = [
            f'{result["name"]} ({result["vintage"]})' for result in results_filtered]
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
    supply = results.json()
    in_stock = []
    consumed_stock = []
    locations = search_wine_locations_for_content()
    consumed_id = [loc for loc in locations if "Consumed" in loc][0].split("id: ")[1]
    for item in supply:
        if item["physical_location_id"] == consumed_id:
            consumed_stock.append(item)
        else:
            in_stock.append(item)
    # There only are consumed wines (or none at all), so reject attempt to consume
    if len(in_stock) == 0:
        return False, f"No non-consumed supply found for {name} ({vintage})."
    if len(in_stock) != 1:
        return False, f"Expected to find exactly one non-consumed supply for {name} ({vintage})" + \
            f", but found {len(in_stock)}."
    
    # Add a consumed version when we don't have one already
    if len(consumed_stock) == 0:
        to_consume = in_stock[0].copy()
        to_consume["physical_location_id"] = consumed_id
        to_consume["quantity"] = 1
        to_consume["upc_vintage_sd_id"] = None  # Ensure a new entry is created
        response = requests.post(f"http://localhost:8282/wine_supplies", json=to_consume)
        if response.status_code != 201:
            return False, f"Failed to create consumed supply for {name} ({vintage}): {response.text}"
        in_stock[0]["quantity"] -= 1
        if in_stock[0]["quantity"] <= 0:
            response = requests.delete(
                f"http://localhost:8282/wine_supplies/{in_stock[0]['upc_vintage_sd_id']}")
            if response.status_code != 200:
                return False, f"Failed to delete supply for {name} ({vintage}) after consuming last bottle: {response.text}"
        else:
            response = requests.patch(
                f"http://localhost:8282/wine_supplies/quantity",
                json={
                    "bottle_id": in_stock[0]["upc_vintage_sd_id"],
                    "new_quantity": in_stock[0]["quantity"]
                })
            if response.status_code != 200:
                return False, f"Failed to update supply quantity for {name} ({vintage}): {response.text}"
        return True, None

    # We already have a consumed version, so just increase quantity there and decrease in stock quantity
    consumed = consumed_stock[0]
    in_stock = in_stock[0]
    consumed["quantity"] += 1
    in_stock["quantity"] -= 1
    if in_stock["quantity"] <= 0:
        response = requests.delete(
            f"http://localhost:8282/wine_supplies/{in_stock['upc_vintage_sd_id']}")
        if response.status_code != 200:
            return False, f"Failed to delete supply for {name} ({vintage}) after consuming last bottle: {response.text}"
    else:
        response = requests.patch(
            f"http://localhost:8282/wine_supplies/quantity",
            json={
                "bottle_id": in_stock["upc_vintage_sd_id"],
                "new_quantity": in_stock["quantity"]
            })
        if response.status_code != 200:
            return False, f"Failed to update supply quantity for {name} ({vintage}): {response.text}"
    response = requests.patch(
        f"http://localhost:8282/wine_supplies/quantity",
        json={
            "bottle_id": consumed["upc_vintage_sd_id"],
            "new_quantity": consumed["quantity"]
        })
    if response.status_code != 200:
        return False, f"Failed to update consumed supply quantity for {name} ({vintage}): {response.text}"
    return True, None


def create_bottle_entry(name: str, vintage: str | None = None, upc_barcode_id: str | None = None, vendor: str | None = None,
                        region_id: str | None = None, pct_alcohol: str | None = None, drink_by_date: str | None = None,
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
        "region_id": region_id,
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
