""" Generate the actual spreadsheet """
from app.spreadsheet.tabs import (
    generate_by_drink_by_date_tab, generate_by_food_pairing_tab, generate_by_grape_variety_tab,
    generate_by_keyword_tab, generate_by_region_tab, generate_by_type_tab, generate_consumed_tab,
    generate_keyword_summary, generate_by_location_tab, generate_easy_wine_tab
)

TAB_MAP = {
    "Types": generate_by_type_tab,
    "Regions": generate_by_region_tab,
    "Grape Varieties": generate_by_grape_variety_tab,
    "Keywords": generate_by_keyword_tab,
    "Food Pairings": generate_by_food_pairing_tab,
    "Drink-By Date": generate_by_drink_by_date_tab,
    "Locations": generate_by_location_tab,
    "Easy Wines": generate_easy_wine_tab,
    "Consumed": generate_consumed_tab,
    "Keyword Summary": generate_keyword_summary,
}