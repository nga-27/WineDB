""" Handler for countries """
import time
from typing import Union, Tuple

from app.cmd_app.api_utils.countries import create_country
from .utils import BottleHandler


def process_country_creation(name: Union[str, None], country_id: Union[str, None],
                            bottler: BottleHandler) -> Union[str, None]:
    """ Creates a new country entry if needed and returns the country ID """
    if name is None:
        # User chose to skip entering a country
        return None
    if country_id is not None:
        # Country already exists, we'll do the linkage by returning the existing ID
        return country_id
    # Create new country entry and return new ID
    new_country_id, was_successful = create_country_entry(name, bottler)
    if was_successful:
        return new_country_id
    bottler.ui_manager.add_text_content(
        f"\r\n\033[31mSorry, something went wrong adding another country of {name}.\033[39m")
    bottler.ui_manager.add_text_content(f"\r\nError: {new_country_id}\r\n")
    time.sleep(2)
    return None


def create_country_entry(name: str, bottler: BottleHandler) -> Tuple[str, bool]:
    """ Creates a new country entry and returns the new country ID """
    time.sleep(1)
    bottler.ui_manager.add_text_content(f"\r\nCreating new country entry for '{name}'...")
    new_country = {
        "name": name,
        "description": None
    }
    bottler.ui_manager.add_text_content("\r\n")
    time.sleep(1)
    new_country['description'] = bottler.handle_input("Description? ", none_on_skip=True)

    new_country_id, was_successful = create_country(
        new_country["name"],
        new_country["description"]
    )
    if not was_successful:
        # new_country_id in this case will actually be the error message, so we return that for
        # logging and debugging purposes
        return new_country_id, False
    return new_country_id, True
