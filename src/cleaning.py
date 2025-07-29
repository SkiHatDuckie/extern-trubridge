"""src/cleaning.py"""

import pandas as pd

NOT_APPLICABLE_PATTERN = r"(^\(X\)$)|(^\*{5}$)"

def count_missing_cells(df: pd.DataFrame) -> int:
    """Returns the number of cells with missing data."""
    na_count = sum(sum(df[col].astype(str).str.count(NOT_APPLICABLE_PATTERN)) for col in df)
    return df.isnull().sum().sum() + na_count

def fill_missing_cells(df: pd.DataFrame) -> pd.DataFrame:
    """Fills all missing cells with '-1' to signify the absence."""
    df = df.replace(NOT_APPLICABLE_PATTERN, "-1", regex=True)
    return df.fillna("-1")

def count_duplicate_rows(df: pd.DataFrame) -> int:
    """Returns the number of rows that are the exact same as a previous one."""
    return df.duplicated().sum()

def drop_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Drops all duplicate rows from the dataframe."""
    return df.drop_duplicates()

def drop_rows_except(value, series_key: str, df: pd.DataFrame) -> pd.DataFrame:
    """Precondition: Assumes `value` is the correct type for `df[series_key]`.

    Drops all rows that do not match `value` in the series."""
    try:
        return df[df[series_key] == value]
    except KeyError as ex:
        raise KeyError("'series_key' does not exist.") from ex

def match_series(pattern: str, series: pd.Series) -> bool:
    """Returns `True` if all entries in the `series` match the `pattern`, or are -1."""
    return series.astype("string").str.match(pattern).all()

def validate_column_types(df: pd.DataFrame) -> pd.DataFrame:
    """Replaces each column with the expected type."""
    date_pattern = r"(^\d{2}\/\d{2}\/\d{4}$)|(^-1$)"
    float_pattern = r"(^(?!\.{2,}\s)[0-9±%,.\"]+$)|(^-1$)"
    for col in df:
        if df[col].dtype == "object":
            if match_series(date_pattern, df[col]):
                df[col] = pd.to_datetime(df[col], errors="coerce")
            elif match_series(float_pattern, df[col]):
                df[col] = df[col].astype("string").str.replace(r"[,±%\"]", "", regex=True)
                df[col] = df[col].astype("float64")
            else:
                df[col] = df[col].astype("string")
    return df

def trim_excess_space(df: pd.DataFrame) -> pd.DataFrame:
    """Removes unnecessary quotes and whitespace from all series of type string."""
    for col in df:
        if df[col].dtype == "string":
            df[col] = df[col].str.strip()
    return df
