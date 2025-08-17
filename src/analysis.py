"""src/analysis.py"""

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
# import numpy as np
import pandas as pd
# import seaborn as sns

import util

def describe_anxiety_trends(df: pd.DataFrame, group: str):
    """Prints basic stats on every numerical column in `df`,
    partitioned by the 'Subgroup' column, excluding reports by state."""
    print(f"{group}:")
    subgroups = df["Subgroup"].loc[df["Group"] == group].unique()
    for subgroup in subgroups:
        print(f"\t{subgroup}:")
        subgroup_data = df.loc[df["Subgroup"] == subgroup, "Value":]
        util.print_with_indentation(subgroup_data.describe(), num_tabs=2)

def graph_anxiety_trends(df: pd.DataFrame, group: str) -> Figure:
    """Graphs the percentage of individuals who reported having anxiety within `group`
    over time. If a group contains multiple subgroups, then each subgroup will be given
    its own line."""
    subgroups = df["Subgroup"].loc[df["Group"] == group].unique()
    fig, ax = plt.subplots(figsize=(14, 5))
    for subgroup in subgroups:
        subgroup_df = df.loc[df["Subgroup"] == subgroup]
        subgroup_df = subgroup_df.set_index("Time Period Start Date")
        ax.plot(subgroup_df.index, subgroup_df["Value"])

    ax.legend(subgroups)
    plt.title(group, fontsize=20)
    plt.xlabel("Time Period Start Date", fontsize=15)
    plt.ylabel("Value", fontsize=15)
    return fig
