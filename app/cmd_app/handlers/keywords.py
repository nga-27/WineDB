""" Handlers for keywords-related actions in the terminal UI. """
import time
from typing import Union, Tuple, List

from app.cmd_app.api_utils.keywords import search_keywords_for_content, create_keyword
from .utils import BottleHandler


def process_keyword_adding_input(bottler: BottleHandler) -> Tuple[List[str], List[str]]:
    """ Prompts user for grape variety information and processes it """
    keyword_ids: List[str] = []
    keyword_names: List[str] = []
    search_results = search_keywords_for_content("")
    if len(search_results) > 0:
        bottler.ui_manager.add_text_content("\r\nHere are some keywords:")
        bottler.ui_manager.add_text_content("\r\n")
        for i, name in enumerate(search_results):
            actual_name, _ = name.split(", id: ")
            bottler.ui_manager.add_text_content(f"\t - [{i+1}] {actual_name}")
        bottler.ui_manager.add_text_content("\r\n")
        time.sleep(0.5)
    yes_to_add = bottler.handle_input(
        "Do you want to add any keywords or generic tasting notes to this bottle? \033[36m[Y/n]\033[39m ")
    if yes_to_add is not None and "n" in yes_to_add.lower():
        return [], []
    num_keywords = bottler.handle_input(
        "\033[36mHOW MANY\033[39m keywords / generic tasting notes do you want to add? ")
    if num_keywords is None or not num_keywords.isdigit() or int(num_keywords) <= 0:
        return [], []
    for i in range(1, int(num_keywords) + 1):
        bottler.ui_manager.clear_content()
        keyword_name, keyword_id = process_keyword_input(bottler, i)
        if not keyword_name:
            continue
        if keyword_name is not None and keyword_id is None:
            # If we have a name but no ID, we need to create a new keyword entry
            new_keyword_id, was_successful = create_keyword_entry(keyword_name, bottler)
            if was_successful:
                keyword_id = new_keyword_id
            else:
                bottler.ui_manager.add_text_content(
                    f"\r\n\033[31mSorry, something went wrong adding the keyword '{keyword_name}.\033[39m")
                bottler.ui_manager.add_text_content(f"\r\nError: {new_keyword_id}\r\n")
                time.sleep(2)
                continue
        if keyword_id is not None:
            keyword_ids.append(keyword_id)
            keyword_names.append(keyword_name)
    return keyword_names, keyword_ids


def process_keyword_input(bottler: BottleHandler, keyword_list_id: int) -> Tuple[Union[str, None], Union[str, None]]:
    """ Prompts user for countries and processes it, including searching and supply increase options
    
    Returns:
        name (str or None): The name of the linked model, or None if skipped
        id (str or None): The ID of the linked model if it already exists,
                    or None if it needs to be created or was skipped
    """
    name = bottler.handle_input(f"\r\nName of keyword #{keyword_list_id} (-s to search): ")
    search_partial = name.strip() if name is not None else ""
    if len(search_partial) == 0:
        return None, None
    if search_partial.isdigit() and int(search_partial) >= 1:
        search_results = search_keywords_for_content("")
        if int(search_partial) > len(search_results):
            bottler.ui_manager.add_text_content(
                f"\r\n\033[31mInvalid selection. Expected a number between 1 and {len(search_results)}.\033[39m")
            time.sleep(2)
            return None, None
        name = search_results[int(search_partial)-1]
        split_name, split_id = name.split(", id: ")
        bottler.ui_manager.add_text_content(f"\r\nSelected keyword: {split_name.strip()}")
        time.sleep(1)
        return split_name.strip(), split_id.strip()
    if "-s" in search_partial:
        search_partial = search_partial.replace("-s", "").strip()
        search_results = search_keywords_for_content(search_partial)
        bottler.ui_manager.add_text_content("\r\n")
        for i, name_found in enumerate(search_results):
            actual_name, _ = name_found.split(", id: ")
            bottler.ui_manager.add_text_content(f"\t - [{i+1}] {actual_name}")
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


def create_keyword_entry(name: str, bottler: BottleHandler) -> Tuple[str, bool]:
    """ Creates a new wine keyword entry and returns the new wine keyword ID """
    time.sleep(1)
    bottler.ui_manager.add_text_content(f"\r\nCreating new wine keyword entry for '{name}'...")
    new_keyword = {
        "name": name,
        "description": None,
    }
    bottler.ui_manager.add_text_content("\r\n")
    time.sleep(1)
    new_keyword['description'] = bottler.handle_input("Description? ", none_on_skip=True)

    new_keyword_id, was_successful = create_keyword(
        new_keyword["name"],
        new_keyword["description"],
    )
    if not was_successful:
        # new_keyword_id in this case will actually be the error message, so we return that for
        # logging and debugging purposes
        return new_keyword_id, False
    return new_keyword_id, True
