"""src/analysis.py"""

# import numpy as np
import pandas as pd

import util

def describe_anxiety_trends(df: pd.DataFrame):
    """Prints basic stats on every numerical column in `df`,
    partitioned by the 'Subgroup' column, excluding reports by state."""
    groups = df["Group"].unique()
    groups = filter(lambda g: g != "By State", groups)
    for group in groups:
        print(f"{group}:")
        subgroups = df["Subgroup"].loc[df["Group"] == group].unique()
        for subgroup in subgroups:
            print(f"\t{subgroup}:")
            subgroup_data = df.loc[df["Subgroup"] == subgroup, "Value":]
            util.print_with_indentation(subgroup_data.describe(), num_tabs=2)
