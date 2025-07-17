"""src/cleaning.py"""

import pandas as pd

def count_missing_cells(df: pd.DataFrame) -> int:
    """Returns the number of cells with missing data."""
    return df.isnull().sum().sum()

def fill_missing_cells(df: pd.DataFrame) -> pd.DataFrame:
    """Fills all missing cells with '-1' to signify the absence."""
    return df.fillna(-1)

def count_duplicate_rows(df: pd.DataFrame) -> int:
    """Returns the number of rows that are the exact same as a previous one."""
    return df.duplicated().sum()

def drop_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Drops all duplicate rows from the dataframe."""
    return df.drop_duplicates()

def validate_column_types(df: pd.DataFrame) -> pd.DataFrame:
    """Replaces each column with the expected type."""
    string_columns = ("Indicator", "Group", "State", "Subgroup", "Phase", "Time Period Label",
                      "Confidence Interval", "Quartile Range")
    datetime_columns = ("Time Period Start Date", "Time Period End Date")
    for col in string_columns:
        df[col] = df[col].astype("string")
    for col in datetime_columns:
        df[col] = pd.to_datetime(df[col])
    return df
