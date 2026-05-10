import time
from typing import Tuple

from terminal_ui_lite import TerminalUILite

from app.cmd_app.api_utils.bottles import (
    search_supply_for_content, decrease_bottle_supply
)
from .utils import BottleHandler
from .bottles import process_vintage_input


def consume_handler(ui_manager: TerminalUILite) -> bool:
    """consume_handler

    Handles the consume command - allows user to mark a bottle as consumed

    Args:
        ui_manager (TerminalUILite): ui manager instance

    Returns:
        bool: on success of marking bottle as consumed
    """
    ui_manager.add_text_content(
        "\r\nCool, let's DRINK a bottle! (This will mark the bottle as consumed in the database)\r\n")
    time.sleep(1)
    ui_manager.clear_content()
    time.sleep(0.5)
    process_consumption_input_data(ui_manager)
    time.sleep(2)
    return True

##################################

def process_consumption_input_data(ui_manager: TerminalUILite) -> None:
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
            search_results = search_supply_for_content(name=name, by_barcode=True)
            if len(search_results) == 0:
                bottler.ui_manager.add_text_content(f"\r\nNo wine supply found matching UPC barcode '{name}'. Resetting.")
                time.sleep(2)
                return "", None, False
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
                    vintage_response = bottler.handle_input("Should we consume this bottle from the supply? [Y/n] ")
                    if vintage_response is not None and \
                        (len(vintage_response) == 0 or vintage_response.lower() in ["y", "yes"]):
                        was_successful, error_message = decrease_bottle_supply(name, vintage)
                        if was_successful:
                            bottler.ui_manager.add_text_content(f"\r\n\033[32mConsumed a bottle of {name} ({vintage}) from the supply!\033[39m")
                            needs_entry = False
                        else:
                            bottler.ui_manager.add_text_content(f"\r\n\033[31mSorry, something went wrong consuming a bottle of {name} ({vintage}) from the supply.\033[39m")
                            bottler.ui_manager.add_text_content(f"\r\nError: {error_message}\r\n")
                            time.sleep(5)
                        time.sleep(2)
                
            else:
                bottler.ui_manager.add_text_content(
                    f"\r\n\033[33mCouldn't find a bottle to consume named '{name_and_vintage}'\033[39m")
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
                vintage_response = bottler.handle_input("Should we consume this bottle from the supply? [Y/n] ")
                if vintage_response is not None and \
                    (len(vintage_response) == 0 or vintage_response.lower() in ["y", "yes"]):
                    was_successful, error_message = decrease_bottle_supply(name, vintage)
                    if was_successful:
                        bottler.ui_manager.add_text_content(f"\r\n\033[32mConsumed a bottle of {name} ({vintage}) from the supply!\033[39m")
                        needs_entry = False
                    else:
                        bottler.ui_manager.add_text_content(f"\r\n\033[31mSorry, something went wrong consuming a bottle of {name} ({vintage}) from the supply.\033[39m")
                        bottler.ui_manager.add_text_content(f"\r\nError: {error_message}\r\n")
                    time.sleep(2)
        else:
            bottler.ui_manager.add_text_content(
                f"\r\n\033[33mCouldn't find a bottle to consume named '{name_and_vintage}'\033[39m")
            name = name_and_vintage
            time.sleep(2)
    return name, vintage, needs_entry
