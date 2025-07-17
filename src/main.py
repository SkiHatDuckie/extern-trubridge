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
    return df

CWD = os.getcwd()
ANXIETY_TRENDS_DATA_PATH = CWD + "/data/raw/Indicators_of_Anxiety_or_Depression\
_Based_on_Reported_Frequency_of_Symptoms_During_Last_7_Days.csv"
CLEAN_ANXIETY_TRENDS_PATH = CWD + "/data/clean/anxiety_trends.csv"

def save_clean_dataframe(df: pd.DataFrame) -> None:
    """Saves `df` as a .csv."""
    dest_path = CWD + "/data/clean"
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    df.to_csv(CLEAN_ANXIETY_TRENDS_PATH)

if __name__ == "__main__":
    args = init_argument_parser().parse_args()
    anxiety_trends_dataframe = pd.read_csv(ANXIETY_TRENDS_DATA_PATH)
    # print_five_rows(anxiety_trends_dataframe)
    if args.clean:
        clean_anxiety_trends = clean_dataset(anxiety_trends_dataframe)
        print("Saving data to", CLEAN_ANXIETY_TRENDS_PATH)
        save_clean_dataframe(clean_anxiety_trends)
    else:
        pass  # Do data analysis here
