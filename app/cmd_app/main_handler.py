""" main handler for the cmd_app """
import time
from typing import Any

from terminal_ui_lite import TerminalUILite

from app.cmd_app.utils.api import handle_get_payload
from app.cmd_app.utils.constants import PrintColor
from app.cmd_app.handlers import bottle_handler, grape_handler

# from cmd_app.utils.title_page import show_title
# from cmd_app.utils.file_io import copy_from_cloud, error_handler, push_to_cloud

DEFAULT_CALLBACK_DATA = "ASDFAKSDLJ;FASDFLKJHASDLFKjBNALSKJDfH"
CALLBACK_DATA = DEFAULT_CALLBACK_DATA

OPTION_STATES = {
    "b": "bottle",
    "bottle": "bottle",
    "g": "grape",
    "grape": "grape",
    "q": "exit",
    "quit": "exit",
    "e": "exit",
    "exit": "exit",
}

def exit_handler(ui_manager: TerminalUILite) -> bool:
    """ Handles exiting the program """
    # print(f"\r\nWe'll start to {PrintColor.YELLOW}EXIT{PrintColor.NORMAL}...")
    ui_manager.add_text_content("\r\nExiting...")
    time.sleep(1)
    return False


ACTION_FUNCTIONS = {
    "bottle": bottle_handler,
    "grape": grape_handler,
    "exit": exit_handler,
}


def __callback_function(data: Any) -> None:
    global CALLBACK_DATA
    CALLBACK_DATA = data


def what_to_do_options(ui_manager: TerminalUILite) -> str:
    """ Prompts user to potential SplitWiser actions """
    matched = None
    while matched is None:
        ui_manager.clear_content()
        time.sleep(0.5)
        ui_manager.add_text_content("What would you like to do? Options include:\r\n\r\n")

        ui_manager.add_text_content(f"\t- Add {PrintColor.GREEN}GRAPE VARIETIES{PrintColor.NORMAL} (g or grape)")
        ui_manager.add_text_content(f"\t- Add {PrintColor.MAGENTA}BOTTLES{PrintColor.NORMAL} (b or bottle)")
        ui_manager.add_text_content(f"\t- {PrintColor.YELLOW}EXIT{PrintColor.NORMAL} (e or exit, q or quit)")
        ui_manager.add_text_content("\r\n")
        ui_manager.add_input_content("\r\nSo... what would you like to do? ", __callback_function)

        global CALLBACK_DATA
        while CALLBACK_DATA is not None and CALLBACK_DATA == DEFAULT_CALLBACK_DATA:
            time.sleep(0.1)
        ui_manager.clear_content()
        time.sleep(1)
        passed = CALLBACK_DATA
        CALLBACK_DATA = DEFAULT_CALLBACK_DATA
        if passed is None or len(passed) == 0:
            ui_manager.add_text_content(f"\r\nI'm sorry, but '{passed}' is not a valid input. Please try again...\r\n")
            time.sleep(2)
            continue
        passed = passed.lower().strip()
        matched = OPTION_STATES.get(passed[0])
        if not matched:
            ui_manager.add_text_content(f"\r\nI'm sorry, but '{passed}' is not a valid input. Please try again...\r\n")
            time.sleep(2)
        ui_manager.clear_content()
    return matched

###################################################

def run(base_url: str, ui_manager: TerminalUILite) -> None:
    """run

    Runs the main command loop of options

    Args:
        base_url (str): api base url
    """
    is_running = True
    while is_running:
        action = what_to_do_options(ui_manager)
        is_running = ACTION_FUNCTIONS[action](ui_manager)


def boot_up_sync(pwd: str) -> bool:
    """boot_up_sync

    Boots up the app + copies the xlsx db file from the cloud

    Args:
        pwd (str): current working directory path

    Returns:
        bool: on success of copying xlsx db file from cloud location
    """
    # show_title()
    # is_successful = copy_from_cloud(pwd)
    # if not is_successful:
    #     error_handler("Missing path files. Exiting...")
    #     time.sleep(2)
    #     return False
    return True


def close_out_sync(pwd: str) -> bool:
    """cloud_out_sync

    Closes down the app + copies the xlsx db file to the cloud

    Args:
        pwd (str): current working directory path

    Returns:
        bool: on success of copying xlsx db file to cloud location
    """
    # is_successful = push_to_cloud(pwd)
    # if not is_successful:
    #     error_handler("Copying to cloud issue.")
    #     time.sleep(2)
    #     return False
    return True


def startup(base_url: str, ui_manager: TerminalUILite) -> None:
    """startup

    Boots up the api and DB portion, and continues to try hitting the API until it is ready

    Args:
        base_url (str): base url of the API
    """
    has_succeeded = False
    while not has_succeeded:
        try:
            handle_get_payload(f"{base_url}/start", skip_response=True)
            has_succeeded = True
        except: # pylint: disable=bare-except
            pass
        time.sleep(1)


def shutdown(base_url: str, ui_manager: TerminalUILite) -> None:
    """shutdown

    Shuts down the api (which saves the local DB to the xlsx db file)

    Args:
        base_url (str): base url of the API
    """
    print("\r\nShutting down...")
    handle_get_payload(f"{base_url}/shutdown", skip_response=True)
