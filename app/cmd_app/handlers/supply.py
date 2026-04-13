""" Supply handler for viewing ONLY """

import time

from terminal_ui_lite import TerminalUILite

from app.cmd_app.api_utils.bottles import search_supply_for_content
from .utils import BottleHandler


def view_handler(ui_manager: TerminalUILite) -> bool:
    """ Handles viewing Wine Supply """
    bottler = BottleHandler(ui_manager)
    bottler.ui_manager.add_text_content("\r\nViewing wine supply...")
    time.sleep(1)
    supply_content = search_supply_for_content()
    if len(supply_content) == 0:
        bottler.ui_manager.add_text_content("No supply found.")
        time.sleep(2)
    else:
        bottler.ui_manager.add_text_content("Current supply:\r\n")
        for supply in supply_content:
            bottler.ui_manager.add_text_content(f"\t- {supply}")
        bottler.ui_manager.add_text_content(f"\r\n\r\n")
        bottler.handle_input("Press enter to continue...", none_on_skip=True)
    return True
