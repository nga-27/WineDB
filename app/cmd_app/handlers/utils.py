""" Utils for handlers """
from typing import Any, Union
import time

from terminal_ui_lite import TerminalUILite


DEFAULT_CALLBACK_DATA = "ASDFAKSDLJ;FASDFLKJHASDLFKjBNALSKJDfH"

class BottleHandler:
    """ Callback handling class"""
    # pylint: disable=too-few-public-methods

    def __init__(self, ui_manager: TerminalUILite):
        self.ui_manager = ui_manager
        self.__callback_data = DEFAULT_CALLBACK_DATA

    def handle_input(self, prompt: str, none_on_skip: bool = False) -> Union[str, None]:
        """ Prompts user for input and returns it """
        tries = 0
        while tries < 3:
            self.ui_manager.add_input_content(prompt, self.__callback_function, input_timeout=120)
            while self.__callback_data is not None and \
                self.__callback_data == DEFAULT_CALLBACK_DATA:
                time.sleep(0.1)
            tries += 1
            data = self.__callback_data
            self.__callback_data = DEFAULT_CALLBACK_DATA
            if data is not None:
                break
        if tries == 3:
            self.ui_manager.add_text_content(
                "\r\n\033[31mSorry, something went wrong getting your input. Please try again later.\033[39m\r\n") # pylint: disable=line-too-long
            return None
        if none_on_skip and data is not None and len(data) == 0:
            return None
        return data

    def __callback_function(self, data: Any) -> None:
        self.__callback_data = data
