import os
import subprocess
import threading
import time

from terminal_ui_lite import TerminalUILite

from static.ascii_generator import ascii_generator
from app.db.database import get_db_interface
from app.cmd_app.main_handler import (
    run, startup, shutdown
)

BASE_URL = "http://localhost:8282"
BASE_PORT = 8282

def run_api():
    subprocess.run(
        ["uvicorn", "app.app:app", "--log-level=warning", f"--port={BASE_PORT}"],
        check=False
    )


def run_cmd_prompts():
    """ Run the command prompt 'UI' """
    ui_manager = TerminalUILite(ascii_generator)
    startup(BASE_URL, ui_manager)
    run(BASE_URL, ui_manager)
    shutdown(BASE_URL, ui_manager)


def run_app():
    db_interface = get_db_interface()
    db_interface.create_db_and_tables()

    t_api = threading.Thread(target=run_api, name='API', daemon=True)
    t_ui = threading.Thread(target=run_cmd_prompts, name='Command-Based UI', daemon=True)

    t_api.start()
    time.sleep(0.1)
    t_ui.start()

    t_ui.join()
    t_api.join()

    time.sleep(1)
    print("Goodbye!")
    time.sleep(2)


if __name__ == "__main__":
    run_app()
