import time
from typing import Union, Tuple

from app.cmd_app.api_utils.regions import create_region
from app.cmd_app.api_utils.countries import search_countries_for_content
from app.cmd_app.handlers.countries import process_region_creation
from .generic import process_linking_input
from .utils import BottleHandler


def process_region_creation(name: Union[str, None], region_id: Union[str, None],
                            bottler: BottleHandler) -> Union[str, None]:
    """ Creates a new region entry if needed and returns the region ID """
    if name is None:
        # User chose to skip entering a region
        return None
    if region_id is not None:
        # Region already exists, we'll do the linkage by returning the existing ID
        return region_id
    # Create new region entry and return new ID
    new_region_id, was_successful = create_region_entry(name, bottler)
    if was_successful:
        return new_region_id
    bottler.ui_manager.add_text_content(
        f"\r\n\033[31mSorry, something went wrong adding another region of {name}.\033[39m")
    bottler.ui_manager.add_text_content(f"\r\nError: {new_region_id}\r\n")
    time.sleep(2)
    return None


def create_region_entry(name: str, bottler: BottleHandler) -> Tuple[str, bool]:
    """ Creates a new region entry and returns the new region ID """
    time.sleep(1)
    bottler.ui_manager.add_text_content(f"\r\nCreating new region entry for '{name}'...")
    new_region = {
        "name": name,
        "country_id": None,
        "description": None
    }
    bottler.ui_manager.add_text_content("\r\n")
    time.sleep(1)
    new_region['description'] = bottler.handle_input("Description? ", none_on_skip=True)
    country_name, country_id = process_linking_input(
        bottler, "country", search_countries_for_content)
    country_id = process_region_creation(country_name, country_id, bottler)
    new_region["country_id"] = country_id

    new_region_id, was_successful = create_region(
        new_region["name"],
        new_region["country_id"],
        new_region["description"]
    )
    if not was_successful:
        # new_region_id in this case will actually be the error message, so we return that for
        # logging and debugging purposes
        return new_region_id, False
    return new_region_id, True
