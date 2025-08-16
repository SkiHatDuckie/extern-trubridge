"""src/analysis.py"""

import matplotlib.pyplot as plt
# import numpy as np
import pandas as pd
# import seaborn as sns

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

def graph_anxiety_trends(df: pd.DataFrame, group: str):
    """Graphs the percentage of individuals who reported having anxiety within `group`
    over time. If a group contains multiple subgroups, then each subgroup will be given
    its own line."""
    _ = plt.subplots(figsize=(16, 5))
    subgroups = df["Subgroup"].loc[df["Group"] == group].unique()
    for subgroup in subgroups:
        subgroup_df = df.loc[df["Subgroup"] == subgroup]
        subgroup_df = subgroup_df.set_index("Time Period Start Date")
        plt.plot(subgroup_df.index, subgroup_df["Value"])

    plt.title(group, fontsize=20)
    plt.xlabel("Time Period Start Date", fontsize=15)
    plt.ylabel("Value", fontsize=15)
    ticks = list(subgroup_df.index)
    plt.xticks(ticks, rotation=45)
    plt.show()
