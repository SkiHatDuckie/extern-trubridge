"""src/main.py"""

import argparse
import os

import pandas as pd

import cleaning

def init_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ExternProject",
                                     description="TODO: Add desc")
    parser.add_argument("--clean",
                        action="store_true",
                        help="Download, clean and integrate the raw datasets before use.")
    return parser

def print_five_rows(df: pd.DataFrame) -> None:
    print("First 5 rows:")
    print(df.head())
    print("\nDataFrame information:")
    print(df.info())

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    print("Filling", cleaning.count_missing_cells(df), "cells with -1...")
    df = cleaning.fill_missing_cells(df)
    print("Dropping", cleaning.count_duplicate_rows(df), "duplicate rows...")
    df = cleaning.drop_duplicate_rows(df)
    print("Correcting data types...")
    df = cleaning.validate_column_types(df)
    # print("Trimming extra spaces and quotes...")
    # df = cleaning.trim_extra_space(df)
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
            print_five_rows(dataframe)
            clean_dataframe = clean_dataset(dataframe)
            print("DEBUG: AFTER CLEANING:")
            print_five_rows(clean_dataframe)

            print("Saving data to", CLEAN_DATA_PATHS[idx], "\n")
            save_clean_dataframe(clean_dataframe, CLEAN_DATA_PATHS[idx])
    else:
        pass  # Do data analysis here
