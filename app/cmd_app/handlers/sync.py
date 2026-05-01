import os
from datetime import datetime
from typing import List
import time

import pandas as pd
import requests
from terminal_ui_lite import TerminalUILite

from app.db.database import WineSupply
from app.spreadsheet.generator import TAB_MAP


def sync_handler(ui_manager: TerminalUILite) -> bool:
    """sync_handler

    Syncs the xlsx db file with the cloud location

    Args:
        ui_manager (TerminalUILite): ui manager instance

    Returns:
        bool: on success of syncing with cloud location
    """
    ui_manager.add_text_content("Starting spreadsheet sync...")
    
    # Get all wine supplies from database
    wines_data: List[dict] = requests.get("http://localhost:8282/wine_supplies/joined").json()
    wines: List[WineSupply] = [WineSupply.model_validate(wine_data) for wine_data in wines_data]
    
    if not wines or len(wines) == 0:
        ui_manager.add_text_content("\033[31mNo wines found in database to export.\033[39m")
        time.sleep(2)
        return True
    
    ui_manager.add_text_content(f"Found {len(wines)} wines to export.")
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"WineDB_Export_{timestamp}.xlsx")
    
    # Create Excel writer and generate each tab
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for tab_name, tab_generator in TAB_MAP.items():
            ui_manager.add_text_content(f"Generating '{tab_name}' tab...")
            tab_data = tab_generator(wines)
            
            if tab_data:
                df = pd.DataFrame(tab_data)
                # Sanitize sheet name (Excel limit: 31 chars, no special chars)
                safe_sheet_name = tab_name[:31].replace("/", "-").replace("\\", "-")
                df.to_excel(writer, sheet_name=safe_sheet_name, index=False)
                ui_manager.add_text_content(f"\033[32m'{tab_name}' tab generated with {len(tab_data)} records.\033[39m")
            else:
                ui_manager.add_text_content(f"\033[33mTab '{tab_name}' returned no data.\033[39m")
    
    ui_manager.add_text_content(f"Spreadsheet exported to: {output_path}")
    time.sleep(10)
    return True