from typing import Any, Union
import time

from terminal_ui_lite import TerminalUILite


DEFAULT_CALLBACK_DATA = "ASDFAKSDLJ;FASDFLKJHASDLFKjBNALSKJDfH"

class BottleHandler:
    """ Callback handling class"""

    def __init__(self, ui_manager: TerminalUILite):
        self.ui_manager = ui_manager
        self.__callback_data = DEFAULT_CALLBACK_DATA
    
    def handle_input(self, prompt: str, none_on_skip: bool = False) -> Union[str, None]:
        """ Prompts user for input and returns it """
        self.ui_manager.add_input_content(prompt, self.__callback_function)
        while self.__callback_data is not None and self.__callback_data == DEFAULT_CALLBACK_DATA:
            time.sleep(0.1)
        data = self.__callback_data
        self.__callback_data = DEFAULT_CALLBACK_DATA
        if none_on_skip and data is not None and len(data) == 0:
            return None
        return data
    
    def __callback_function(self, data: Any) -> None:
        self.__callback_data = data
