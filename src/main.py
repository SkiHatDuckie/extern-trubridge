"""src/main.py"""

import argparse
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

ANXIETY_TRENDS_DATA_PATH = "data/raw/Indicators_of_Anxiety_or_Depression\
_Based_on_Reported_Frequency_of_Symptoms_During_Last_7_Days.csv"
CLEAN_ANXIETY_TRENDS_PATH = "data/clean/anxiety_trends.csv"

if __name__ == "__main__":
    args = init_argument_parser().parse_args()
    anxiety_trends_dataframe = pd.read_csv(ANXIETY_TRENDS_DATA_PATH)
    # print_five_rows(anxiety_trends_dataframe)
    if args.clean:
        clean_anxiety_trends = clean_dataset(anxiety_trends_dataframe)
        print("Saving data to", CLEAN_ANXIETY_TRENDS_PATH)
        clean_anxiety_trends.to_csv(CLEAN_ANXIETY_TRENDS_PATH)
    else:
        pass  # Do data analysis here
