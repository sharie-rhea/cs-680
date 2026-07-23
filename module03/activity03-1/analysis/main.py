# Sharie Rhea
# 07.21.26
# SNHU CS680

import heapq
import os
import timeit

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_data(file_path: str) -> tuple[list, list, list]:
    """
    Parses data from a '|' separated value file and returns 3 lists with differing field orders.

    Parameters:
        file_path: str - the path of the data file to load from
    Returns: 3 lists of tuples with the fields in different orders for sorting purposes
    """
    print(f"Loading file {file_path}...")
    # keep_default_na=False handles blank strings
    df = pd.read_csv(file_path, sep="|", keep_default_na=False)
    # convert to a list of dicts
    dictionary = df.to_dict("records")
    # convert to list of tuples for heapq module
    # NOTE: I have placed the validation field second so that if the first field results in a tie,
    # the validation fields are compared next for sorting
    by_key = [(row["key"], row["validation"], row["data-a"], row["data-b"]) for row in dictionary]
    by_data_a = [(row["data-a"], row["validation"], row["key"], row["data-b"]) for row in dictionary]
    by_data_b = [(row["data-b"], row["validation"], row["key"], row["data-a"]) for row in dictionary]
    return by_key, by_data_a, by_data_b


def heapsort(iterable: list) -> list:
    """
    Sorts a list of values by creating a heap, then popping all elements off the heap in order.

    Parameters:
        iterable: list - the list of values to sort
    Returns: list of sorted values
    """
    heapq.heapify(iterable)
    return [heapq.heappop(iterable) for _ in range(len(iterable))]


def run_analysis():
    results = []
    trials = 10

    data_dir = "data"
    for file in os.scandir(data_dir):
        by_key, by_data_a, by_data_b = load_data(file.path)
        n = len(by_key)
        fields: dict[str, list[tuple]] = {"key": by_key, "data-a": by_data_a, "data-b": by_data_b}

        # time trials!
        for name, data in fields.items():
            print(f"\tSorting {file.name} by {name}...")
            # make sure to copy data so we are re-sorting every time
            timer = timeit.Timer(lambda: heapsort(data[:]))
            total_time = timer.timeit(number=trials)
            avg_time = total_time / trials
            time_per_elem = avg_time / n
            results.append(
                {
                    "File": file.name,
                    "Size": n,
                    "Field": name,
                    "Time": total_time,
                    "AvgTime": avg_time,
                    "TimePerElem": time_per_elem,
                    "State": "unsorted",
                }
            )
            print(results[-1])
        # see if starting with sorted data is any faster
        for name, data in fields.items():
            print(f"\tSorting {file.name} by {name}...")
            data.sort()
            timer = timeit.Timer(lambda: heapsort(data))
            total_time = timer.timeit(number=trials)
            avg_time = total_time / trials
            time_per_elem = avg_time / n
            results.append(
                {
                    "File": file.name,
                    "Size": n,
                    "Field": name,
                    "Time": total_time,
                    "AvgTime": avg_time,
                    "TimePerElem": time_per_elem,
                    "State": "sorted",
                }
            )
            print(results[-1])

    return pd.DataFrame(results)


if __name__ == "__main__":
    # NOTE: uncomment to re-run analysis
    # df_results = run_analysis()
    # df_results.to_csv("analysis_results.csv")

    df_results = pd.read_csv("analysis_results.csv")
    # convert time to microseconds
    df_results["TimePerElem"] = df_results["TimePerElem"] * 1_000_000

    # set Seaborn theme
    sns.set_theme(style="white")

    # pivot table for sorted/unsorted
    df_pivot = df_results.pivot_table(
        index=["Size", "Field"], columns="State", values="TimePerElem", aggfunc="mean"
    ).reset_index()

    sizes = sorted(df_pivot["Size"].unique())
    fields = ["key", "data-a", "data-b"]
    n_sizes = len(sizes)
    n_fields = len(fields)

    # bar positioning
    x = np.arange(n_sizes)
    total_width = 0.8
    bar_width = total_width / n_fields

    fig, ax = plt.subplots(figsize=(12, 6))
    palette = sns.color_palette("viridis", n_colors=n_fields)

    # overlays
    for i, field in enumerate(fields):
        field_df = df_pivot[df_pivot["Field"] == field].set_index("Size").reindex(sizes)

        unsorted_vals = field_df["unsorted"].fillna(0).values
        sorted_vals = field_df["sorted"].fillna(0).values
        # to remove errors
        assert isinstance(unsorted_vals, np.ndarray) and isinstance(sorted_vals, np.ndarray)

        offset = x + (i - n_fields / 2 + 0.5) * bar_width

        # unsorted/background bars
        ax.bar(
            offset,
            unsorted_vals,
            bar_width,
            label=f"{field} (Unsorted)",
            color=palette[i],
            alpha=0.35,
            hatch="//",
            edgecolor=palette[i],
            linewidth=1,
        )

        # sorted/foreground bars
        ax.bar(
            offset,
            sorted_vals,
            bar_width,
            label=f"{field} (Sorted)",
            color=palette[i],
            edgecolor="white",
            linewidth=0.8,
        )

        # numeric labels for unsorted
        for pos, u in zip(offset, unsorted_vals):
            if u > 0:
                ax.annotate(
                    f"{u:.1f}",
                    xy=(pos, u),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    fontweight="bold",
                )

        # numeric labels for sorted
        for pos, s in zip(offset, sorted_vals):
            if s > 0:
                ax.annotate(
                    f"{s:.1f}",
                    xy=(pos, s),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    fontweight="bold",
                )

    # formatting
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.set_xlabel("Dataset Size (n)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Average Time per Element (μs)", fontsize=12, fontweight="bold")
    ax.set_title(
        "Heapsort: Unsorted vs. Sorted Average Time per Element",
        fontsize=16,
        fontweight="bold",
        pad=25,
    )

    ax.legend(title="Field & State", loc="upper left")

    sns.despine()
    plt.tight_layout()
    plt.savefig("time_per_elem_overlay.png", dpi=300, bbox_inches="tight")
    plt.show()
