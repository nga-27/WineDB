""" Utilities for API calls for bottles """
from typing import List, Tuple, Union
import logging

import requests

from app.logging_config import LOGGER_NAME
from .locations import search_wine_locations_for_content

# pylint: disable=line-too-long, broad-except,too-many-arguments, too-many-locals,
# pylint: disable=too-many-return-statements, too-many-branches, too-many-statements

def search_supply_for_content(name: str | None = None, vintage: str | None = None,
                              omit_consumed: bool = True, by_barcode: bool = False) -> List[str]:
    """ Placeholder function to search for content based on user input """
    consumed_location_id = "NOT-A-REAL-ID"
    if omit_consumed:
        consumed_location_id_list = search_wine_locations_for_content("Consumed")
        if len(consumed_location_id_list) > 0:
            consumed_location_id = consumed_location_id_list[0].split("id: ")[1]
    if name is None:
        results = requests.get("http://localhost:8282/wine_supplies", timeout=5)
        results_filtered = [\
            result for result in results.json() \
                if result["physical_location_id"] != consumed_location_id]
        result_names = [
            f'{result["name"]} ({result["vintage"]}) - {result["vendor"]} - \
                QTY: {result["quantity"]}' for result in results_filtered]
        return result_names
    if by_barcode:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}&by_barcode=true", timeout=5)
        results_filtered = [
            result for result in results.json() \
                if result["physical_location_id"] != consumed_location_id]
        result_names = [
            f'{result["name"]} ({result["vintage"]})' for result in results_filtered]
        return result_names
    if vintage:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}&vintage={vintage}", timeout=5)
    else:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}", timeout=5)
    results_filtered = [
        result for result in results.json() \
            if result["physical_location_id"] != consumed_location_id]
    result_names = [f'{result["name"]} ({result["vintage"]})' for result in results_filtered]
    return result_names


def increase_bottle_supply(name: str, vintage: str) -> Tuple[bool, Union[None, str]]:
    """ Placeholder function to increase bottle supply based on user input """
    if vintage:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}&vintage={vintage}", timeout=5)
    else:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}", timeout=5)
    if len(results.json()) != 1:
        return False, "Expected to find exactly one supply for " + \
            f"{name} ({vintage}), but found {len(results.json())}."
    supply = results.json()[0]
    bottle_id = supply["upc_vintage_sd_id"]
    response = requests.patch(
        "http://localhost:8282/wine_supplies/quantity",
        json={"bottle_id": bottle_id, "new_quantity": supply["quantity"] + 1}, timeout=5)
    return response.status_code == 200, response.text


def handle_ratings_averaging(
        consumed_obj: dict, new_rating: Union[str, None]
        ) -> Tuple[Union[str, None], Union[str, None]]:
    """ Handle averaging of ratings when consuming a bottle that has already been
    consumed before
    """
    if new_rating is None:
        return consumed_obj["drank_rating"], consumed_obj["drank_rating_raw"]
    if consumed_obj["drank_rating"] is None:
        return new_rating, new_rating
    try:
        old_ratings = [
            float(r.strip()) for r in consumed_obj["drank_rating"].split(",") if len(r.strip()) > 0]
        new_rating_float = float(new_rating)
        all_ratings = old_ratings + [new_rating_float]
        averaged_rating = sum(all_ratings) / len(all_ratings)
        return f"{averaged_rating:.1f}", ','.join(f"{r:.1f}" for r in all_ratings)
    except ValueError:
        return new_rating, new_rating  # If ratings aren't valid floats, just use the new rating


def handle_notes_appending(
        consumed_obj: dict, new_notes: Union[str, None], note_type: str
        ) -> Union[str, None]:
    """ Handle appending of notes when consuming a bottle that has already been consumed before """
    if new_notes is None:
        return consumed_obj[note_type]
    if consumed_obj[note_type] is None:
        return new_notes
    return consumed_obj[note_type] + "; " + new_notes


def move_bottle_location(
        name: str, vintage: str, to_location_id: str) -> Tuple[bool, Union[None, str]]:
    """ Placeholder function to move a bottle based on user input """
    # For simplicity, we'll just decrease supply from current location and increase supply in
    # new location. In a real implementation, we would want to update the physical_location_id
    # of the existing supply entry instead
    if vintage:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}&vintage={vintage}", timeout=5)
    else:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}", timeout=5)
    supply = results.json()
    results = requests.get("http://localhost:8282/locations", timeout=5)
    consumed_location_id = "NOT-A-REAL-ID"
    for location in results.json():
        if location["name"] == "Consumed":
            consumed_location_id = location["location_id"]
            break
    supply = [s for s in supply if s["physical_location_id"] != consumed_location_id]
    if len(supply) == 0:
        return False, f"No supply found for {name} ({vintage})."
    if len(supply) > 1:
        return False, \
            f"Expected to find exactly one supply for {name} ({vintage}), but found {len(supply)}."
    supply = supply[0]
    response = requests.patch("http://localhost:8282/wine_supplies/move", params={
        "bottle_id": supply["upc_vintage_sd_id"],
        "new_location_id": to_location_id
    }, timeout=5)
    if response.status_code != 200:
        return False, f"Failed to move supply for {name} ({vintage}): {response.text}"
    return True, None


def decrease_bottle_supply(
        name: str, vintage: str, ratings: Union[str, None] = None,
        rating_notes: Union[str, None] = None, drank_date: Union[str, None] = None,
        drank_event_notes: Union[str, None] = None
        ) -> Tuple[bool, Union[None, str]]:
    """ Placeholder function to decrease bottle supply based on user input """
    if vintage:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}&vintage={vintage}", timeout=5)
    else:
        results = requests.get(f"http://localhost:8282/wine_supplies?name={name}", timeout=5)
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
        # pylint: disable=line-too-long
        to_consume = in_stock[0].copy()
        # Many-to-many relationships
        grape_response = requests.get(
            f"http://localhost:8282/grape_varieties?upc_vintage_sd_id={to_consume['upc_vintage_sd_id']}", timeout=5)
        if grape_response.status_code == 200:
            to_consume["grape_ids"] = [grape["variety_id"] for grape in grape_response.json()]
        food_pairing_response = requests.get(
            f"http://localhost:8282/food_pairings?upc_vintage_sd_id={to_consume['upc_vintage_sd_id']}", timeout=5)
        if food_pairing_response.status_code == 200:
            to_consume["food_pairing_ids"] = [
                pairing["pairing_id"] for pairing in food_pairing_response.json()]
        keyword_response = requests.get(
            f"http://localhost:8282/keywords?upc_vintage_sd_id={to_consume['upc_vintage_sd_id']}", timeout=5)
        if keyword_response.status_code == 200:
            to_consume["keyword_ids"] = [
                keyword["keyword_id"] for keyword in keyword_response.json()]

        to_consume["physical_location_id"] = consumed_id
        to_consume["quantity"] = 1
        to_consume["upc_vintage_sd_id"] = None  # Ensure a new entry is created
        ratings, ratings_raw = handle_ratings_averaging(to_consume, ratings)
        to_consume["drank_rating"] = ratings
        to_consume["drank_rating_raw"] = ratings_raw
        to_consume["drank_rating_notes"] = rating_notes
        to_consume["drank_date"] = drank_date
        to_consume["drank_event_notes"] = drank_event_notes
        response = requests.post("http://localhost:8282/wine_supplies", json=to_consume, timeout=5)
        if response.status_code != 201:
            return False, \
                f"Failed to create consumed supply for {name} ({vintage}): {response.text}"
        in_stock[0]["quantity"] -= 1
        if in_stock[0]["quantity"] <= 0:
            response = requests.delete(
                f"http://localhost:8282/wine_supplies/{in_stock[0]['upc_vintage_sd_id']}", timeout=5)
            if response.status_code != 200:
                return False, \
                    f"Failed to delete supply for {name} ({vintage}) after consuming last bottle: {response.text}"
        else:
            response = requests.patch(
                "http://localhost:8282/wine_supplies/quantity",
                json={
                    "bottle_id": in_stock[0]["upc_vintage_sd_id"],
                    "new_quantity": in_stock[0]["quantity"]
                }, timeout=5)
            if response.status_code != 200:
                return False, \
                    f"Failed to update supply quantity for {name} ({vintage}): {response.text}"
        return True, None

    # We already have a consumed version, so just increase quantity there and decrease in stock quantity
    consumed = consumed_stock[0]
    in_stock = in_stock[0]
    consumed["quantity"] += 1
    in_stock["quantity"] -= 1
    if in_stock["quantity"] <= 0:
        response = requests.delete(
            f"http://localhost:8282/wine_supplies/{in_stock['upc_vintage_sd_id']}", timeout=5)
        if response.status_code != 200:
            return False, \
                f"Failed to delete supply for {name} ({vintage}) after consuming last bottle: {response.text}"
    else:
        response = requests.patch(
            "http://localhost:8282/wine_supplies/quantity",
            json={
                "bottle_id": in_stock["upc_vintage_sd_id"],
                "new_quantity": in_stock["quantity"]
            }, timeout=5)
        if response.status_code != 200:
            return False, \
                f"Failed to update supply quantity for {name} ({vintage}): {response.text}"

    ratings, ratings_raw = handle_ratings_averaging(consumed, ratings)
    consumed["drank_rating"] = ratings
    consumed["drank_rating_raw"] = ratings_raw
    consumed["drank_rating_notes"] = handle_notes_appending(
        consumed, rating_notes, "drank_rating_notes")
    consumed["drank_date"] = handle_notes_appending(
        consumed, drank_date, "drank_date")
    consumed["drank_event_notes"] = handle_notes_appending(
        consumed, drank_event_notes, "drank_event_notes")
    response = requests.patch(
        "http://localhost:8282/wine_supplies/quantity",
        json={
            "bottle_id": consumed["upc_vintage_sd_id"],
            "new_quantity": consumed["quantity"],
            "drank_rating": consumed["drank_rating"],
            "drank_rating_raw": consumed["drank_rating_raw"],
            "drank_rating_notes": consumed["drank_rating_notes"],
            "drank_event_notes": consumed["drank_event_notes"],
            "drank_date": consumed["drank_date"],
        }, timeout=5)
    if response.status_code != 200:
        return False, \
            f"Failed to update consumed supply quantity for {name} ({vintage}): {response.text}"
    return True, None


def create_bottle_entry(
        name: str, vintage: str | None = None, upc_barcode_id: str | None = None,
        vendor: str | None = None, region_id: str | None = None, pct_alcohol: str | None = None,
        drink_by_date: str | None = None, tasting_notes: str | None = None,
        obtainment_note: str | None = None, other_notes: str | None = None,
        physical_location_id: str | None = None, wine_type_id: str | None = None,
        country_id: str | None = None, grape_ids: List[str] | None = None,
        keyword_ids: List[str] | None = None, food_pairing_ids: List[str] | None = None,
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
        "keyword_ids": keyword_ids,
        "food_pairing_ids": food_pairing_ids
    }
    logger.info("Creating bottle entry with payload: %s", payload)
    try:
        response = requests.post("http://localhost:8282/wine_supplies", json=payload, timeout=5)
    except Exception as exc:
        logger.error("Error occurred while creating bottle entry: %s", exc)
        return False, f"Error occurred while creating bottle entry: {exc}"
    logger.info("Create bottle entry response: %s - %s", response.status_code, response.text)
    return response.status_code == 201, response.text
