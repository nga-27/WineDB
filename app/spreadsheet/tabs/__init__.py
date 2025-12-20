""" Tabs for organizing wine data in spreadsheets """
from .by_drink_by_date import generate_by_drink_by_date_tab
from .by_food_pairing import generate_by_food_pairing_tab
from .by_grape_variety import generate_by_grape_variety_tab
from .by_keyword import generate_by_keyword_tab, generate_keyword_summary
from .by_region import generate_by_region_tab
from .by_type import generate_by_type_tab
from .consumed import generate_consumed_tab