"""src/main.py"""

import argparse
import inspect
import json
import os

import matplotlib.pyplot as plt
import pandas as pd

import analysis
import cleaning
import util

def init_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ExternProject",
                                     description="TODO: Add desc")
    parser.add_argument("--clean",
                        action="store_true",
                        help="Download, clean and integrate the raw datasets before use.")
    parser.add_argument("--report",
                        action="store_true",
                        help="Display a quality report for each dataset.")
    return parser

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    print("Correcting column data types...")
    df = cleaning.validate_column_types(df)

    numeric_cols = df.select_dtypes(include=["number"]).columns
    print(f"Filling {cleaning.count_missing_cells(df[numeric_cols])} cells with mean...")
    df = cleaning.replace_nan_with_mean(df)

    print(f"Filling {cleaning.count_missing_cells(df)} cells with -1...")
    df = df.fillna("-1")

    print(f"Dropping {cleaning.count_duplicate_rows(df)} duplicate rows...")
    df = df.drop_duplicates()

    print("Trimming excess spaces and quotes...")
    df = cleaning.trim_excess_space(df)

    return df

def report_data_quality(df: pd.DataFrame):
    """Does a check of the `df` for any missing values, incorrect data types, and more."""
    print("Quality Report")
    print(f"Missing values: {cleaning.count_missing_cells(df)}")
    print(f"Data Types:\n {df.dtypes}")
    print(f"Duplicate Rows: {cleaning.count_duplicate_rows(df)}")
    print(f"Summary Stats:\n {df.describe()}\n")
    for col in df.select_dtypes(include=["string"]).columns:
        print(f"Unique values in {col}:\n", df[col].unique(), "\n")

def anxiety_trends_special_clean(df: pd.DataFrame) -> pd.DataFrame:
    func_name = inspect.currentframe().f_code.co_name
    print(f"{func_name}: Dropping irrelevant data...")
    df = cleaning.drop_rows_except("Symptoms of Anxiety Disorder", "Indicator", df)

    print(f"{func_name}: Dropping rows where Phase == -1...")
    df = df.loc[df["Phase"] != "-1"]
    # At this point, these columns are now redundant
    return df.drop(columns=["Indicator"])

def american_community_survey_special_clean(df: pd.DataFrame) -> pd.DataFrame:
    func_name = inspect.currentframe().f_code.co_name
    print(f"{func_name}: Dropping divider rows...")
    df = df[~df["Label (Grouping)"].str.isupper()]

    percent_cols = util.get_percent_columns(df)
    invalid_percentage_cnt = cleaning.count_invalid_percents(df[percent_cols])
    replacement = 0.0
    print(f"{func_name}: Replacing {invalid_percentage_cnt} invalid percentage values with \
{replacement}%.")
    df = cleaning.replace_invalid_percents(replacement, df)
    return df

CWD = os.getcwd()
RAW_DATA_PATHS = (CWD + "/data/raw/Indicators_of_Anxiety_or_Depression_Based_on_Reported\
_Frequency_of_Symptoms_During_Last_7_Days.csv",
                  CWD + "/data/raw/ACSDP5Y2023.DP05-2025-07-25T220355.csv",
                  CWD + "/data/raw/ACSDP5Y2023.DP02-2025-07-25T213601.csv")
CLEAN_DATA_PATHS = (CWD + "/data/clean/anxiety_trends.csv",
                    CWD + "/data/clean/demographics.csv",
                    CWD + "/data/clean/household.csv")

def save_clean_dataframe(df: pd.DataFrame, dest_path: os.path) -> None:
    """Saves `df` as a .csv. Additionally saves the column datatypes in a
    .json file, as CSV files do not hold onto this information."""
    dest_folder = CWD + "/data/clean"
    dtypes_path = dest_path[:-4] + ".json"
    dtypes_df = df.dtypes.to_frame('dtypes').reset_index()
    dtypes_dict = dtypes_df.set_index('index')['dtypes'].astype(str).to_dict()
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
    with open(dtypes_path, "w", encoding="utf-8") as f:
        json.dump(dtypes_dict, f)
    df.to_csv(dest_path, index=False)

def read_csv_with_dtypes(src_path: str) -> pd.DataFrame:
    """Reads a cleaned dataset at `src_path`, appending the correct data types for
    each column. Fails if either cleaned .csv or .json is missing."""
    dtypes_path = src_path[:-4] + ".json"
    with open(dtypes_path, "r", encoding="utf-8") as f:
        dtypes = json.load(f)
        non_datetime_dtypes = util.filter_dict_by_value(dtypes, "datetime64[ns]")
        datetime_cols = util.get_keys_with_value(dtypes, "datetime64[ns]")
        return pd.read_csv(src_path, dtype=non_datetime_dtypes, parse_dates=datetime_cols)

def run_cleaning_process():
    """Postcondition: Datasets will now have a cleaned counterpart in `data/clean`."""
    for idx, raw_path in enumerate(RAW_DATA_PATHS):
        dataframe = pd.read_csv(raw_path)
        print(f"Cleaning {raw_path}")
        clean_dataframe = clean_dataset(dataframe)
        if idx == 0:
            clean_dataframe = anxiety_trends_special_clean(clean_dataframe)
        else:
            clean_dataframe = american_community_survey_special_clean(clean_dataframe)
        print(f"Saving data to {CLEAN_DATA_PATHS[idx]}")
        print(f"Saving datatypes to {CLEAN_DATA_PATHS[idx][:-4]}.json\n")
        save_clean_dataframe(clean_dataframe, CLEAN_DATA_PATHS[idx])

def run_quality_report():
    """Precondition: Cleaned datasets have already been created."""
    try:
        for data_path in CLEAN_DATA_PATHS:
            dataframe = read_csv_with_dtypes(data_path)
            print(f"{data_path}")
            report_data_quality(dataframe)
    except FileNotFoundError as ex:
        raise FileNotFoundError("Data must be cleaned first!") \
            from ex.with_traceback(None)

def run_data_analysis():
    """Precondition: Cleaned datasets have already been created."""
    try:
        anxiety_df, demographics_df, household_df = \
            [read_csv_with_dtypes(data_path) for data_path in CLEAN_DATA_PATHS]
        analysis.describe_anxiety_trends(anxiety_df)
        analysis.graph_anxiety_trends(anxiety_df, "By Age")
        plt.show()
    except FileNotFoundError as ex:
        raise FileNotFoundError("Data must be cleaned first!") \
            from ex.with_traceback(None)

if __name__ == "__main__":
    args = init_argument_parser().parse_args()
    if args.clean:
        run_cleaning_process()
    if args.report:
        run_quality_report()
    run_data_analysis()
