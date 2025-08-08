"""src/main.py"""

import argparse
import inspect
import os

import pandas as pd

import cleaning
import util

def init_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ExternProject",
                                     description="TODO: Add desc")
    parser.add_argument("--clean",
                        action="store_true",
                        help="Download, clean and integrate the raw datasets before use.")
    parser.add_argument("--describe",
                        action="store_true",
                        help="Display the summary tables for each dataset.")
    return parser

def print_five_rows(df: pd.DataFrame) -> None:
    print("First 5 rows:")
    print(df.head())
    print("\nDataFrame information:")
    print(df.info())

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

def anxiety_trends_special_clean(df: pd.DataFrame) -> pd.DataFrame:
    func_name = inspect.currentframe().f_code.co_name
    print(f"{func_name}: Dropping irrelevant data...")
    df = cleaning.drop_rows_except("Symptoms of Anxiety Disorder", "Indicator", df)
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
    """Saves `df` as a .csv."""
    dest_folder = CWD + "/data/clean"
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
    df.to_csv(dest_path)

if __name__ == "__main__":
    args = init_argument_parser().parse_args()
    if args.clean:
        for idx, raw_path in enumerate(RAW_DATA_PATHS):
            dataframe = pd.read_csv(raw_path)
            print(f"Cleaning {raw_path}")
            clean_dataframe = clean_dataset(dataframe)
            if idx == 0:
                clean_dataframe = anxiety_trends_special_clean(clean_dataframe)
            else:
                clean_dataframe = american_community_survey_special_clean(clean_dataframe)

            print(f"Saving data to {CLEAN_DATA_PATHS[idx]}\n")
            save_clean_dataframe(clean_dataframe, CLEAN_DATA_PATHS[idx])
    if args.describe:
        try:
            for idx, data_path in enumerate(CLEAN_DATA_PATHS):
                dataframe = pd.read_csv(data_path)
                print(f"{data_path}")
                print(dataframe.describe(), "\n")
        except FileNotFoundError as ex:
            raise FileNotFoundError("Data must be cleaned first!") \
                from ex.with_traceback(None)

    # Do data analysis here
