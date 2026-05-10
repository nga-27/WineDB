""" Handlers for bottle-related actions in the command-line application. """
import time
from typing import Tuple
import uuid

from terminal_ui_lite import TerminalUILite

from app.cmd_app.api_utils.bottles import (
    search_supply_for_content, increase_bottle_supply, create_bottle_entry
)
from app.cmd_app.api_utils.regions import search_regions_for_content, get_country_from_region
from app.cmd_app.api_utils.wine_types import search_wine_types_for_content
from app.cmd_app.api_utils.countries import search_countries_for_content
from app.cmd_app.api_utils.locations import search_wine_locations_for_content
from .food_pairings import process_food_pairing_adding_input
from .keywords import process_keyword_adding_input
from .generic import process_linking_input
from .regions import process_region_creation
from .countries import process_country_creation
from .wine_types import process_wine_type_creation
from .locations import process_wine_location_creation
from .grapes import process_grape_variety_input
from .utils import BottleHandler


def bottle_handler(ui_manager: TerminalUILite) -> bool:
    """ Handles adding bottles """
    ui_manager.add_text_content("\r\nCool, let's add a bottle")
    time.sleep(1)
    ui_manager.clear_content()
    time.sleep(0.5)
    process_bottle_input_data(ui_manager)
    return True


##########################################################

def process_name_input(bottler: BottleHandler) -> Tuple[str, str | None, bool]:
    """ Prompts user for name and processes it, including searching and supply increase options """
    vintage = None
    needs_entry = True
    name = bottler.handle_input("What's the name of the wine? (-s for search) ")
    if name is None or len(name.strip()) == 0:
        return "", None, False
    if len(name.strip()) == 13 and name.strip().isdigit():
        barcode_response = bottler.handle_input(f"\r\nIs '{name}' a UPC barcode? [Y/n] ")
        if barcode_response is not None and (len(barcode_response) == 0 or barcode_response.lower() in ["y", "yes"]):
            name = name.strip()
            search_results = search_supply_for_content(name, by_barcode=True)
            if len(search_results) == 0:
                bottler.ui_manager.add_text_content(f"\r\nNo wine supply found matching UPC barcode '{name}'. Resetting.")
                time.sleep(2)
                return "", None, False
            bottler.ui_manager.add_text_content("\r\n")
            for i, name in enumerate(search_results):
                bottler.ui_manager.add_text_content(f"\t - [{i+1}] {name}")
            bottler.ui_manager.add_text_content("\r\n")
            time.sleep(0.5)

            name_and_vintage = bottler.handle_input("Pick one of these or enter a new name? (type number) ")
            if name_and_vintage.isdigit() and 1 <= int(name_and_vintage) <= len(search_results):
                name_and_vintage = search_results[int(name_and_vintage)-1]
                name = name_and_vintage.split(" (")[0]
                vintage = name_and_vintage.split(" (")[1].split(") - ")[0]
                vintage_response = bottler.handle_input(f"\r\nSame vintage as {vintage}? [Y/n] ")
                if vintage_response is not None and \
                    (len(vintage_response) > 0 and vintage_response.lower() in ["n", "no"]):
                    vintage = None
                if vintage is not None:
                    vintage_response = bottler.handle_input("Should we add another bottle to the supply? [Y/n] ")
                    if vintage_response is not None and \
                        (len(vintage_response) == 0 or vintage_response.lower() in ["y", "yes"]):
                        was_successful, error_message = increase_bottle_supply(name, vintage)
                        if was_successful:
                            bottler.ui_manager.add_text_content(f"\r\n\033[32mAdded another bottle of {name} ({vintage}) to the supply!\033[39m")
                            needs_entry = False
                        else:
                            bottler.ui_manager.add_text_content(f"\r\n\033[31mSorry, something went wrong adding another bottle of {name} ({vintage}) to the supply.\033[39m")
                            bottler.ui_manager.add_text_content(f"\r\nError: {error_message}\r\n")
                        time.sleep(2)
            else:
                bottler.ui_manager.add_text_content(
                    f"\r\nWe'll start a new bottle entry for '{name_and_vintage}'")
                name = name_and_vintage
                time.sleep(2)
    elif "-s" in name:
        search_partial = name.replace("-s", "").strip()
        search_results = search_supply_for_content(search_partial)
        if len(search_results) == 0:
            bottler.ui_manager.add_text_content(f"\r\nNo wine supply found matching '{search_partial}'. Resetting.")
            time.sleep(2)
            return "", None, False
        bottler.ui_manager.add_text_content("\r\n")
        for i, name in enumerate(search_results):
            bottler.ui_manager.add_text_content(f"\t - [{i+1}] {name}")
        bottler.ui_manager.add_text_content("\r\n")
        time.sleep(0.5)

        name_and_vintage = bottler.handle_input("Pick one of these or enter a new name? (type number) ")
        if name_and_vintage.isdigit() and 1 <= int(name_and_vintage) <= len(search_results):
            name_and_vintage = search_results[int(name_and_vintage)-1]
            name = name_and_vintage.split(" (")[0]
            vintage = name_and_vintage.split(" (")[1].replace(")", "")
            vintage_response = bottler.handle_input(f"\r\nSame vintage as {vintage}? [Y/n] ")
            if vintage_response is not None and \
                (len(vintage_response) > 0 and vintage_response.lower() in ["n", "no"]):
                vintage = None
            if vintage is not None:
                vintage_response = bottler.handle_input("Should we add another bottle to the supply? [Y/n] ")
                if vintage_response is not None and \
                    (len(vintage_response) == 0 or vintage_response.lower() in ["y", "yes"]):
                    was_successful, error_message = increase_bottle_supply(name, vintage)
                    if was_successful:
                        bottler.ui_manager.add_text_content(f"\r\n\033[32mAdded another bottle of {name} ({vintage}) to the supply!\033[39m")
                        needs_entry = False
                    else:
                        bottler.ui_manager.add_text_content(f"\r\n\033[31mSorry, something went wrong adding another bottle of {name} ({vintage}) to the supply.\033[39m")
                        bottler.ui_manager.add_text_content(f"\r\nError: {error_message}\r\n")
                    time.sleep(2)
        else:
            bottler.ui_manager.add_text_content(
                f"\r\nWe'll start a new bottle entry for '{name_and_vintage}'")
            name = name_and_vintage
            time.sleep(2)
    return name, vintage, needs_entry


def process_vintage_input(bottler: BottleHandler, name: str, vintage: str | None) -> Tuple[str | None, bool, str | None]:
    """ Prompts user for vintage and processes it, including searching and supply increase options
    
    Returns:
        vintage (str or None): The vintage (year) of the wine, or None if not provided or invalid
        needs_entry (bool): Whether we need to continue to create a new supply entry
        modified name (str or None): The modified name if the user selected an existing supply with
            a different vintage, or None if not modified
    """
    alt_name = None
    if vintage is None:
        vintage = bottler.handle_input("\r\nWhat's the vintage (year)? ")
        if vintage is None or len(vintage.strip()) == 0:
            return None, True, None
        if vintage is not None and len(vintage.strip()) > 0 and not vintage.strip().isdigit():
            bottler.ui_manager.add_text_content(
                f"\r\n\033[31mInvalid vintage (year). Resetting.\033[39m")
            time.sleep(2)
            return None, False, None

        # This should be a valid vintage. Check if it already exists
        if vintage is not None:
            existing_supplies = search_supply_for_content(name)
            for supply in existing_supplies:
                if supply.endswith(f"({vintage})"):
                    vintage_response = bottler.handle_input(
                        f"\r\nA supply with the same name and vintage \033[33m({vintage})already exists\033[39m. Should we add another bottle to the supply? \033[36m[Y/n]\033[39m ")
                    if vintage_response is not None and \
                        (len(vintage_response) == 0 or vintage_response.lower() in ["y", "yes"]):
                        was_successful, error_message = increase_bottle_supply(name, vintage)
                        if was_successful:
                            bottler.ui_manager.add_text_content(f"\r\n\033[32mAdded another bottle of {name} ({vintage}) to the supply!\033[39m")
                        else:
                            bottler.ui_manager.add_text_content(f"\r\n\033[31mSorry, something went wrong adding another bottle of {name} ({vintage}) to the supply.\033[39m")
                            bottler.ui_manager.add_text_content(f"\r\nError: {error_message}\r\n")
                        time.sleep(2)
                        return None, False, None
                    else:
                        bottler.ui_manager.add_text_content(
                            f"\r\nWe'll start a new bottle entry for '{name} ({vintage})'")
                        time.sleep(2)
                        uuid_str = str(uuid.uuid4())[:8]
                        alt_name = f"{name} -- {uuid_str}"
    return vintage, True, alt_name


def process_bottle_input_data(ui_manager: TerminalUILite) -> None:
    """ Prompts user for bottle information and processes it """
    vintage = None
    name = None
    bottler = BottleHandler(ui_manager)
    ui_manager.add_text_content("\r\nLet's start with the basics...\r\n")
    time.sleep(1)

    name, vintage, needs_entry = process_name_input(bottler)
    if not needs_entry:
        return
    bottler.ui_manager.clear_content()
    time.sleep(0.5)

    vintage, needs_entry, alt_name = process_vintage_input(bottler, name, vintage)
    if not needs_entry:
        return
    if alt_name is not None:
        name = alt_name
    bottler.ui_manager.clear_content()
    time.sleep(0.5)        

    winery = bottler.handle_input("\r\nWhich vendor/winery produced it? ")
    barcode = bottler.handle_input("\r\nWhat's the UPC barcode (hit 'enter' to skip)? ", none_on_skip=True)
    quantity_response = bottler.handle_input("\r\nHOW MANY bottles are we adding? (default 1) ")
    quantity = 1
    if quantity_response.isdigit() and int(quantity_response) > 0:
        quantity = int(quantity_response)

    region_name, region_id = process_linking_input(bottler, "region", search_regions_for_content)
    region_id = process_region_creation(region_name, region_id, bottler)
    bottler.ui_manager.clear_content()
    time.sleep(0.5)

    country_name, country_id = get_country_from_region(region_id)
    if country_name is None or country_id is None:
        country_name, country_id = process_linking_input(
            bottler, "country", search_countries_for_content)
        region_id = process_country_creation(country_name, country_id, bottler)
        bottler.ui_manager.clear_content()
        time.sleep(0.5)

    type_name, type_id = process_linking_input(bottler, "wine_type", search_wine_types_for_content)
    type_id = process_wine_type_creation(type_name, type_id, bottler)
    bottler.ui_manager.clear_content()
    time.sleep(0.5)

    grape_names, grape_ids = process_grape_variety_input(bottler)
    bottler.ui_manager.clear_content()
    time.sleep(0.5)

    keyword_names, keyword_ids = process_keyword_adding_input(bottler)
    bottler.ui_manager.clear_content()
    time.sleep(0.5)

    tasting_notes = bottler.handle_input("\r\nAny additional / specific tasting notes? (hit 'enter' to skip) ", none_on_skip=True)
    pct_alcohol = bottler.handle_input("\r\nWhat's the percentage of alcohol? (hit 'enter' to skip) ", none_on_skip=True)
    drink_by_date = bottler.handle_input("\r\nWhat's the drink-by date? (hit 'enter' to skip) ", none_on_skip=True)

    food_pairing_names, food_pairing_ids = process_food_pairing_adding_input(bottler)
    bottler.ui_manager.clear_content()
    time.sleep(0.5)

    obtainment_note = bottler.handle_input("\r\nAny obtainment notes? (hit 'enter' to skip) ", none_on_skip=True)
    other_notes = bottler.handle_input("\r\nAny other notes? (hit 'enter' to skip) ", none_on_skip=True)

    location_name, location_id = process_linking_input(bottler, "physical location", search_wine_locations_for_content)
    location_id = process_wine_location_creation(location_name, location_id, bottler)
    bottler.ui_manager.clear_content()
    time.sleep(0.5)

    # ADD RELATIONSHIPS!!!

    ui_manager.add_text_content(f"\r\nGreat! You entered:\r\n")
    ui_manager.add_text_content(f"\tName: {name}")
    ui_manager.add_text_content(f"\tVintage: {vintage if vintage is not None else '--'}")
    ui_manager.add_text_content(f"\tWinery: {winery if winery is not None else '--'}")
    ui_manager.add_text_content(f"\tWine Type: {type_name if type_name is not None else '--'}")
    ui_manager.add_text_content(f"\tGrapes: {', '.join(grape_names)}")
    ui_manager.add_text_content(f"\tKeywords: {', '.join(keyword_names)}")
    ui_manager.add_text_content(f"\tQuantity: {quantity}")
    ui_manager.add_text_content(f"\tRegion: {region_name if region_name is not None else '--'}")
    ui_manager.add_text_content(f"\tCountry: {country_name if country_name is not None else '--'}")
    ui_manager.add_text_content(f"\t% Alcohol: {pct_alcohol if pct_alcohol is not None else '--'}")
    ui_manager.add_text_content(f"\tDrink-by date: {drink_by_date if drink_by_date is not None else '--'}")
    ui_manager.add_text_content(f"\tTasting notes: {tasting_notes if tasting_notes is not None else '--'}")
    ui_manager.add_text_content(f"\tFood pairings: {', '.join(food_pairing_names)}")
    ui_manager.add_text_content(f"\tObtainment note: {obtainment_note if obtainment_note is not None else '--'}")
    ui_manager.add_text_content(f"\tOther notes: {other_notes if other_notes is not None else '--'}")
    ui_manager.add_text_content(f"\tPhysical location: {location_name if location_name is not None else '--'}")
    ui_manager.add_text_content(f"\tBarcode: {barcode if barcode is not None else '--'}\r\n")

    time.sleep(2)
    should_keep = bottler.handle_input("Should we keep this entry? [Y/n] ")
    if should_keep is not None and (len(should_keep) == 0 or should_keep.lower() in ["y", "yes"]):
        create_bottle_entry_response = create_bottle_entry(
            name=name,
            vintage=vintage,
            upc_barcode_id=barcode,
            vendor=winery,
            region_id=region_id,
            pct_alcohol=pct_alcohol,
            drink_by_date=drink_by_date,
            tasting_notes=tasting_notes,
            obtainment_note=obtainment_note,
            other_notes=other_notes,
            quantity=quantity,
            wine_type_id=type_id,
            country_id=country_id,
            physical_location_id=location_id,
            grape_ids=grape_ids,
            keyword_ids=keyword_ids,
            food_pairing_ids=food_pairing_ids
        )
        if create_bottle_entry_response[0]:
            ui_manager.add_text_content(f"\r\n\033[32mSuccess! Added {name} ({vintage}) to the supply!\033[39m")
        else:
            ui_manager.add_text_content(f"\r\n\033[31mSorry, something went wrong adding {name} ({vintage}) to the supply.\033[39m")
            ui_manager.add_text_content(f"\r\nError: {create_bottle_entry_response[1]}\r\n")
            time.sleep(15)
    else:
        ui_manager.add_text_content("\r\nGot it, discarding this entry.")
    time.sleep(2)
