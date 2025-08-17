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

def print_with_indentation(df: pd.DataFrame, num_tabs: int=1):
    """Prepends `num_tabs` tabs to the end of each line."""
    print("\n".join(["\t" * num_tabs + line for line in str(df).split("\n")]))

def construct_file_name(name: str, prefix: str=None) -> str:
    """Formats a string to represent a file name."""
    pattern = re.compile("[ /]")
    name = pattern.sub("_", name.lower())
    return prefix + name
