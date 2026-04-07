""" Handlers for grape-related actions in the terminal UI. """
import time

from terminal_ui_lite import TerminalUILite


def grape_handler(ui_manager: TerminalUILite) -> bool:
    """ Handles adding grape varieties """
    ui_manager.add_text_content("\r\nAdding grape varieties... (not yet implemented)")
    time.sleep(2)
    return True
