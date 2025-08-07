"""src/util.py"""

import re

import pandas as pd

def get_percent_columns(df: pd.DataFrame) -> list:
    """Returns a list of only the columns that contain percentages."""
    return [col for col in df if re.search(r"Percent$", col)]
