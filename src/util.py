"""src/util.py"""

import re

import pandas as pd

def get_percent_columns(df: pd.DataFrame) -> list:
    """Returns a list of only the columns that contain percentages."""
    return [col for col in df if re.search(r"Percent$", col)]

def filter_dict_by_value(d: dict, val) -> dict:
    """Returns a dict containing all pairs that do not include `target`."""
    return {k: v for k, v in d.items() if val != v}

def get_keys_with_value(d: dict, val) -> list:
    """Returns a list of keys that include `val`."""
    return [k for k, v in d.items() if val == v]
