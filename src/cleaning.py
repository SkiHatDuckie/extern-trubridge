"""src/cleaning.py"""

import numpy as np
import pandas as pd

import util

def count_missing_cells(df: pd.DataFrame) -> int:
    """Returns the number of cells with missing data."""
    return df.isnull().sum().sum()

def count_duplicate_rows(df: pd.DataFrame) -> int:
    """Returns the number of rows that are the exact same as a previous one."""
    return df.duplicated().sum()

def count_invalid_percents(df: pd.DataFrame) -> int:
    """Precondition: All columns in `df` hold values representing percentages.
    
    Returns the number of cells that are not in the valid range of 0-100%."""
    cnt = 0
    for col in df:
        values = df[col].values
        valid_range = values[(0 <= values) & (values <= 100)]
        cnt += sum(df[col].isin(valid_range))
    return cnt

def replace_na_with_nan(df: pd.DataFrame) -> pd.DataFrame:
    """Replaces other values indicating N/A (i.e. `(X)` and `*****`), with `numpy.nan`."""
    not_applicable_pattern = r"(^\(X\)$)|(^\*{2,}$)|(^-$)"
    return df.replace(not_applicable_pattern, np.nan, regex=True)

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
                df[col] = pd.to_datetime(df[col], errors="ignore")
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

def replace_nan_with_mean(df: pd.DataFrame) -> pd.DataFrame:
    """Replaces all missing values with the mean value of the column,
    for all numeric columns."""
    for col in df:
        if pd.api.types.is_numeric_dtype(df[col]):
            values = df[col].values
            mean = np.nanmean(values)
            df[col] = np.where(np.isnan(values), mean, values)
    return df

def replace_invalid_percents(val, df: pd.DataFrame) -> pd.DataFrame:
    """Precondition: `val` is the same type used for representing ALL percent columns."""
    percent_cols = util.get_percent_columns(df)
    df = df.copy()  # Explicitly copy to make numpy happy.
    for col in percent_cols:
        values = df[col].values
        valid_range = values[(0 <= values) & (values <= 100)]
        df.loc[df[col].isin(valid_range), col] = val
    return df
