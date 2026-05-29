import os
import threading
import time

import uvicorn
from terminal_ui_lite import TerminalUILite

from static.ascii_generator import ascii_generator
from app.db.database import get_db_interface
from app.cmd_app.main_handler import (
    run, startup, shutdown
)
from app.logging_config import LOGGING_CONFIG
from seeding.auto_seed import auto_seed

BASE_URL = "http://localhost:8282"
BASE_PORT = 8282

def run_api():
    uvicorn.run(
        "app.app:app",
        host="127.0.0.1",
        port=BASE_PORT,
        log_config=LOGGING_CONFIG,
        log_level="info",
    )


def run_cmd_prompts():
    """ Run the command prompt 'UI' """
    ui_manager = TerminalUILite(ascii_generator)
    startup(BASE_URL, ui_manager)
    run(ui_manager)
    shutdown(BASE_URL, ui_manager)


def run_app():
    db_interface = get_db_interface()
    db_interface.create_db_and_tables()

    t_api = threading.Thread(target=run_api, name='API', daemon=True)
    t_ui = threading.Thread(target=run_cmd_prompts, name='Command-Based UI', daemon=True)

    t_api.start()
    time.sleep(0.1)
    t_ui.start()
    time.sleep(1)
    if not auto_seed():
        print("\r\n\r\n\r\n\r\n\r\n\033[31mDatabase seed FAILED.\033[39m")

    t_ui.join()
    t_api.join()

    time.sleep(1)
    print("Goodbye!")
    time.sleep(2)


if __name__ == "__main__":
    run_app()
