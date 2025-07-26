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

# def trim_extra_space(df: pd.DataFrame) -> pd.DataFrame:
#     """Removes unnecessary quotes from all cells, and then trims away excess whitespace."""
#     pass

def match_series(pattern: str, series: pd.Series) -> bool:
    """Returns `True` if all entries in the `series` match the `pattern`, or are -1."""
    return series.str.match(pattern).all()

def validate_column_types(df: pd.DataFrame) -> pd.DataFrame:
    """Replaces each column with the expected type."""
    date_pattern = r"(^\d{2}/\d{2}/\d{4}$)|(^-1$)"
    for col in df:
        if df[col].dtype == "object":
            if match_series(date_pattern, df[col]):
                df[col] = pd.to_datetime(df[col])
            else:
                df[col] = df[col].astype("string")
    return df
