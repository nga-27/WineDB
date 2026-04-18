""" Handlers for food pairing-related actions in the terminal UI. """
import time
from typing import Union, Tuple, List

from app.cmd_app.api_utils.food_pairings import search_food_pairings_for_content, create_food_pairing
from .utils import BottleHandler


def process_food_pairing_adding_input(bottler: BottleHandler) -> Tuple[List[str], List[str]]:
    """ Prompts user for grape variety information and processes it """
    food_pairing_ids: List[str] = []
    food_pairing_names: List[str] = []
    search_results = search_food_pairings_for_content("")
    if len(search_results) > 0:
        bottler.ui_manager.add_text_content("\r\nHere are some food pairings:")
        bottler.ui_manager.add_text_content("\r\n")
        for i, name in enumerate(search_results):
            bottler.ui_manager.add_text_content(f"\t - [{i+1}] {name}")
        bottler.ui_manager.add_text_content("\r\n")
        time.sleep(0.5)
    yes_to_add = bottler.handle_input(
        "Do you want to add any food pairings to this bottle? [Y/n] ")
    if yes_to_add is not None and "n" in yes_to_add.lower():
        return [], []

    num_food_pairings = bottler.handle_input(
        "HOW MANY food pairings do you want to add? ")
    if num_food_pairings is None or not num_food_pairings.isdigit() or int(num_food_pairings) <= 0:
        return [], []
    for i in range(1, int(num_food_pairings) + 1):
        bottler.ui_manager.clear_content()
        food_pairing_name, food_pairing_id = process_food_pairing_input(bottler, i)
        if not food_pairing_name:
            continue
        if food_pairing_name is not None and food_pairing_id is None:
            # If we have a name but no ID, we need to create a new food pairing entry
            new_food_pairing_id, was_successful = create_food_pairing_entry(food_pairing_name, bottler)
            if was_successful:
                food_pairing_id = new_food_pairing_id
            else:
                bottler.ui_manager.add_text_content(
                    f"\r\n\033[31mSorry, something went wrong adding the food pairing '{food_pairing_name}.\033[39m")
                bottler.ui_manager.add_text_content(f"\r\nError: {new_food_pairing_id}\r\n")
                time.sleep(2)
                continue
        if food_pairing_id is not None:
            food_pairing_ids.append(food_pairing_id)
            food_pairing_names.append(food_pairing_name)
    return food_pairing_names, food_pairing_ids


def process_food_pairing_input(bottler: BottleHandler, food_pairing_list_id: int) -> Tuple[Union[str, None], Union[str, None]]:
    """ Prompts user for countries and processes it, including searching and supply increase options
    
    Returns:
        name (str or None): The name of the linked model, or None if skipped
        id (str or None): The ID of the linked model if it already exists,
                    or None if it needs to be created or was skipped
    """
    name = bottler.handle_input(f"\r\nName of food pairing #{food_pairing_list_id} (-s to search): ")
    search_partial = name.strip() if name is not None else ""
    if len(search_partial) == 0:
        return None, None
    if search_partial.isdigit() and int(search_partial) >= 1:
        search_results = search_food_pairings_for_content("")
        if int(search_partial) > len(search_results):
            bottler.ui_manager.add_text_content(
                f"\r\nInvalid selection. Expected a number between 1 and {len(search_results)}.")
            time.sleep(2)
            return None, None
        name = search_results[int(search_partial)-1]
        split_name, split_id = name.split(", id: ")
        bottler.ui_manager.add_text_content(f"\r\nSelected keyword: {split_name.strip()}")
        time.sleep(1)
        return split_name.strip(), split_id.strip()

    if "-s" in search_partial:
        search_partial = search_partial.replace("-s", "").strip()
        search_results = search_food_pairings_for_content(search_partial)
        bottler.ui_manager.add_text_content("\r\n")
        for i, name_found in enumerate(search_results):
            bottler.ui_manager.add_text_content(f"\t - [{i+1}] {name_found}")
        bottler.ui_manager.add_text_content("\r\n")
        time.sleep(0.5)

        generic = bottler.handle_input(
            f"Pick one of these or enter a new name? (type number or 'enter' to start a new keyword) ")
        if generic.isdigit() and 1 <= int(generic) <= len(search_results):
            name = search_results[int(generic)-1]
            split_name, split_id = name.split(", id: ")
            return split_name.strip(), split_id.strip()
        search_partial = generic.strip()
        
    bottler.ui_manager.add_text_content(
        f"\r\nWe'll start a new keyword entry for '{search_partial}'")
    name = search_partial
    time.sleep(2)
    return name, None


def create_food_pairing_entry(name: str, bottler: BottleHandler) -> Tuple[str, bool]:
    """ Creates a new food pairing entry and returns the new food pairing ID """
    time.sleep(1)
    bottler.ui_manager.add_text_content(f"\r\nCreating new food pairing entry for '{name}'...")
    new_food_pairing = {
        "name": name,
        "description": None,
    }
    bottler.ui_manager.add_text_content("\r\n")
    time.sleep(1)
    new_food_pairing['description'] = bottler.handle_input("Description? ", none_on_skip=True)

    new_food_pairing_id, was_successful = create_food_pairing(
        new_food_pairing["name"],
        new_food_pairing["description"],
    )
    if not was_successful:
        # new_food_pairing_id in this case will actually be the error message, so we return that for
        # logging and debugging purposes
        return new_food_pairing_id, False
    return new_food_pairing_id, True
