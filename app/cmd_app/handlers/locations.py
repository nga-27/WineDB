import time
from typing import Union, Tuple

from app.cmd_app.api_utils.locations import create_wine_location
from .utils import BottleHandler


def process_wine_location_creation(name: Union[str, None], location_id: Union[str, None],
                                   bottler: BottleHandler) -> Union[str, None]:
    """ Creates a new wine location entry if needed and returns the wine location ID """
    if name is None:
        # User chose to skip entering a wine location
        return None
    if location_id is not None:
        # Wine location already exists, we'll do the linkage by returning the existing ID
        return location_id
    # Create new wine location entry and return new ID
    new_location_id, was_successful = create_wine_location_entry(name, bottler)
    if was_successful:
        return new_location_id
    bottler.ui_manager.add_text_content(
        f"\r\n\033[31mSorry, something went wrong adding another wine location of {name}.\033[39m")
    bottler.ui_manager.add_text_content(f"\r\nError: {new_location_id}\r\n")
    time.sleep(2)
    return None


def create_wine_location_entry(name: str, bottler: BottleHandler) -> Tuple[str, bool]:
    """ Creates a new wine location entry and returns the new wine location ID """
    time.sleep(1)
    bottler.ui_manager.add_text_content(f"\r\nCreating new wine location entry for '{name}'...")
    new_location = {
        "name": name,
        "description": None
    }
    bottler.ui_manager.add_text_content("\r\n")
    time.sleep(1)
    new_location['description'] = bottler.handle_input("Description? ", none_on_skip=True)

    new_location_id, was_successful = create_wine_location(
        new_location["name"],
        new_location["description"]
    )
    if not was_successful:
        # new_location_id in this case will actually be the error message, so we return that for
        # logging and debugging purposes
        return new_location_id, False
    return new_location_id, True
