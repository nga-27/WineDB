import time
from typing import Union, Tuple

from app.cmd_app.api_utils.wine_types import create_wine_type
from .utils import BottleHandler


def process_wine_type_creation(name: Union[str, None], type_id: Union[str, None],
                               bottler: BottleHandler) -> Union[str, None]:
    """ Creates a new wine type entry if needed and returns the wine type ID """
    if name is None:
        # User chose to skip entering a wine type
        return None
    if type_id is not None:
        # Wine type already exists, we'll do the linkage by returning the existing ID
        return type_id
    # Create new wine type entry and return new ID
    new_type_id, was_successful = create_wine_type_entry(name, bottler)
    if was_successful:
        return new_type_id
    bottler.ui_manager.add_text_content(
        f"\r\n\033[31mSorry, something went wrong adding another wine type of {name}.\033[39m")
    bottler.ui_manager.add_text_content(f"\r\nError: {new_type_id}\r\n")
    time.sleep(2)
    return None


def create_wine_type_entry(name: str, bottler: BottleHandler) -> Tuple[str, bool]:
    """ Creates a new wine type entry and returns the new wine type ID """
    time.sleep(1)
    bottler.ui_manager.add_text_content(f"\r\nCreating new wine type entry for '{name}'...")
    new_type = {
        "name": name,
        "description": None
    }
    bottler.ui_manager.add_text_content("\r\n")
    time.sleep(1)
    new_type['description'] = bottler.handle_input("Description? ", none_on_skip=True)

    new_type_id, was_successful = create_wine_type(
        new_type["name"],
        new_type["description"]
    )
    if not was_successful:
        # new_type_id in this case will actually be the error message, so we return that for
        # logging and debugging purposes
        return new_type_id, False
    return new_type_id, True
