from typing import List
from importlib.metadata import version

def ascii_generator() -> List[str]:
    text = []
    text.append("\033[35m __    __  ____  ____     ___      ____  ____   __ __    ___  ____   ______   ___   ____   __ __ \033[39m")
    text.append("\033[35m|  |__|  ||    ||    \   /  _]    |    ||    \ |  |  |  /  _]|    \ |      | /   \ |    \ |  |  |    \033[39m")
    text.append("\033[35m|  |  |  | |  | |  _  | /  [_      |  | |  _  ||  |  | /  [_ |  _  ||      ||     ||  D  )|  |  |    \033[39m")
    text.append("\033[35m|  |  |  | |  | |  |  ||    _]     |  | |  |  ||  |  ||    _]|  |  ||_|  |_||  O  ||    / |  ~  |    \033[39m")
    text.append("\033[35m|  `  '  | |  | |  |  ||   [_      |  | |  |  ||  :  ||   [_ |  |  |  |  |  |     ||    \ |___, |    \033[39m")
    text.append("\033[35m \      /  |  | |  |  ||     |     |  | |  |  | \   / |     ||  |  |  |  |  |     ||  .  \|     |    \033[39m")
    text.append("\033[35m  \_/\_/  |____||__|__||_____|    |____||__|__|  \_/  |_____||__|__|  |__|   \___/ |__|\_||____/     \033[39m")
    text.append("")
    text.append(f"{' ' * 33}\033[36mVersion: {version('winedb')} - by nga-27\033[39m")
    text.append("\r\n")
    return text
