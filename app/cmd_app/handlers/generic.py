import time
from typing import Union, Tuple

from app.cmd_app.api_utils.regions import search_regions_for_content
from .utils import BottleHandler


def process_linking_input(bottler: BottleHandler, model: str,
                          search_function: callable) -> Tuple[Union[str, None], Union[str, None]]:
    """ Prompts user for countries and processes it, including searching and supply increase options
    
    Returns:
        name (str or None): The name of the linked model, or None if skipped
        id (str or None): The ID of the linked model if it already exists,
                    or None if it needs to be created or was skipped
    """
    name = bottler.handle_input(f"Which {model} is it? (hit 'enter' to skip, -s for search) ")
    search_partial = name.strip() if name is not None else ""
    if name is None or len(name) == 0:
        return None, None
    if "-s" in name:
        search_partial = name.replace("-s", "").strip()
        search_results = search_function(search_partial)
        bottler.ui_manager.add_text_content("\r\n")
        for i, name in enumerate(search_results):
            bottler.ui_manager.add_text_content(f"\t - [{i+1}] {name}")
        bottler.ui_manager.add_text_content("\r\n")
        time.sleep(0.5)

        generic = bottler.handle_input(
            f"Pick one of these or enter a new name? (type number or 'enter' to start a new {model}) ")
        if generic.isdigit() and 1 <= int(generic) <= len(search_results):
            name = search_results[int(generic)-1]
            split_name, split_id = name.split(", id: ")
            return split_name.strip(), split_id.strip()
        search_partial = generic.strip()
        
    bottler.ui_manager.add_text_content(
        f"\r\nWe'll start a new {model} entry for '{search_partial}'")
    name = search_partial
    time.sleep(2)
    return name, None
