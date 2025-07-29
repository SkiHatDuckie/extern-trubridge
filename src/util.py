"""src/util.py"""

import re

import pandas as pd

def get_percentage_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a `pandas.DataFrame` of only the columns that contain percentages."""
    return df[[col for col in df if re.match(r"Percent$", col)]]
