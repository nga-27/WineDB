""" Handlers for grape-related actions in the terminal UI. """
import time
from typing import Union, Tuple, List

from terminal_ui_lite import TerminalUILite

from app.cmd_app.api_utils.grapes import search_wine_grapes_for_content, create_wine_grape
from app.cmd_app.handlers.regions import process_region_creation
from app.cmd_app.api_utils.regions import search_regions_for_content
from .generic import process_linking_input
from .utils import BottleHandler


def grape_handler(ui_manager: TerminalUILite) -> bool:
    """ Handles adding grape varieties """
    ui_manager.add_text_content("\r\nAdding grape varieties... (not yet implemented)")
    time.sleep(2)
    return True


def process_grape_variety_input(bottler: BottleHandler) -> Tuple[List[str], List[str]]:
    """ Prompts user for grape variety information and processes it """
    grape_ids: List[str] = []
    grape_names: List[str] = []
    num_grapes = bottler.handle_input("How many grape varieties are used? ")
    if num_grapes is None or not num_grapes.isdigit() or int(num_grapes) <= 0:
        return [], []
    for i in range(1, int(num_grapes) + 1):
        bottler.ui_manager.clear_content()
        grape_name, grape_id = process_grape_input(bottler, i)
        if not grape_name:
            continue
        if grape_name is not None and grape_id is None:
            # If we have a name but no ID, we need to create a new grape variety entry
            new_grape_id, was_successful = create_wine_grape_entry(grape_name, bottler)
            if was_successful:
                grape_id = new_grape_id
            else:
                bottler.ui_manager.add_text_content(
                    f"\r\n\033[31mSorry, something went wrong adding the grape variety of {grape_name}.\033[39m")
                bottler.ui_manager.add_text_content(f"\r\nError: {new_grape_id}\r\n")
                time.sleep(2)
                continue
        if grape_id is not None:
            grape_ids.append(grape_id)
            grape_names.append(grape_name)
    return grape_names, grape_ids


def process_grape_input(bottler: BottleHandler, grape_id: int) -> Tuple[Union[str, None], Union[str, None]]:
    """ Prompts user for countries and processes it, including searching and supply increase options
    
    Returns:
        name (str or None): The name of the linked model, or None if skipped
        id (str or None): The ID of the linked model if it already exists,
                    or None if it needs to be created or was skipped
    """
    name = bottler.handle_input(f"\r\nName of grape variety #{grape_id} (-s to search): ")
    search_partial = name.strip() if name is not None else ""
    if name is None or len(name) == 0:
        return None, None
    if "-s" in name:
        search_partial = name.replace("-s", "").strip()
        search_results = search_wine_grapes_for_content(search_partial)
        bottler.ui_manager.add_text_content("\r\n")
        for i, name_found in enumerate(search_results):
            bottler.ui_manager.add_text_content(f"\t - [{i+1}] {name_found}")
        bottler.ui_manager.add_text_content("\r\n")
        time.sleep(0.5)

        generic = bottler.handle_input(
            f"Pick one of these or enter a new name? (type number or 'enter' to start a new grape variety) ")
        if generic.isdigit() and 1 <= int(generic) <= len(search_results):
            name = search_results[int(generic)-1]
            split_name, split_id = name.split(", id: ")
            return split_name.strip(), split_id.strip()
        search_partial = generic.strip()
        
    bottler.ui_manager.add_text_content(
        f"\r\nWe'll start a new grape variety entry for '{search_partial}'")
    name = search_partial
    time.sleep(2)
    return name, None


def create_wine_grape_entry(name: str, bottler: BottleHandler) -> Tuple[str, bool]:
    """ Creates a new wine grape entry and returns the new wine grape ID """
    time.sleep(1)
    bottler.ui_manager.add_text_content(f"\r\nCreating new wine grape entry for '{name}'...")
    new_grape = {
        "name": name,
        "description": None,
        "region_id": None
    }
    bottler.ui_manager.add_text_content("\r\n")
    time.sleep(1)
    new_grape['description'] = bottler.handle_input("Description? ", none_on_skip=True)
    region_name, region_id = process_linking_input(bottler, "region", search_regions_for_content)
    region_id = process_region_creation(region_name, region_id, bottler)

    new_grape_id, was_successful = create_wine_grape(
        new_grape["name"],
        new_grape["description"],
        region_id
    )
    if not was_successful:
        # new_grape_id in this case will actually be the error message, so we return that for
        # logging and debugging purposes
        return new_grape_id, False
    return new_grape_id, True
