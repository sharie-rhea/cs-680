# Sharie Rhea
# 07.14.26
# SNHU CS680

import os
import timeit

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sorts import insertionsort, mergesort, quicksort


def load_data(file_path):
    print(f"Loading file {file_path}...")
    # keep_default_na=False handles blank strings
    df = pd.read_csv(file_path, sep="|", keep_default_na=False)
    # convert to a list of dicts for easier sorting
    return df.to_dict("records")


def run_analysis():
    results = []
    data_dir = "data"
    trials = 3

    algos = {"Insertion": insertionsort, "Merge": mergesort, "Quick": quicksort}

    for file in os.scandir(data_dir):
        rows = load_data(file.path)

        for name, func in algos.items():
            # skip insertion on long lists, just takes forever
            if name == "Insertion" and len(rows) > 1000:
                n = 1000
            else:
                n = len(rows)

            print(f"\tSorting {n} items from {file.name} using {name} Sort...")
            for sort_field in ["key", "data"]:
                # define comparator based on field
                comp = lambda a, b: a[sort_field] < b[sort_field]

                # time trial!
                timer = timeit.Timer(lambda: func(rows[:n], comp))
                total_time = timer.timeit(number=trials)

                avg_time = total_time / trials
                time_per_elem = avg_time / n

                # save results
                results.append(
                    {
                        "File": file.name,
                        "Size": n,
                        "Algo": name,
                        "Field": sort_field,
                        "AvgTime": avg_time,
                        "TimePerElem": time_per_elem,
                    }
                )

    return pd.DataFrame(results)


if __name__ == "__main__":
    # NOTE: uncomment to re-run analysis
    # df_results = run_analysis()
    # print(df_results.to_string(index=False, formatters={"AvgTime": "{:.6f}".format, "TimePerElem": "{:.9f}".format}))
    # df_results.to_csv("analysis_results.csv")

    # plotting for analysis!
    df_results = pd.read_csv("analysis_results.csv")
    # convert times to microseconds
    df_results["TimePerElem"] = df_results["TimePerElem"] * 1_000_000

    # PLOT #1: time per element by dataset size
    sns.set_theme(style="white")
    # create the figure
    plt.figure(figsize=(10, 6))
    chart = sns.barplot(data=df_results, x="Size", y="TimePerElem", hue="Algo", palette="viridis", errorbar=None)

    # add numeric labels above bars
    for container in chart.containers:
        chart.bar_label(container, fmt="%.1f", padding=3, fontsize=10)

    # title and axis labels
    plt.title("Comparison of Algorithm Efficiency: Average Time per Element", fontsize=16, fontweight="bold", pad=25)
    plt.xlabel("Dataset Size (n)", fontsize=12, fontweight="bold")
    plt.ylabel("Average Time per Element (µs)", fontsize=12, fontweight="bold")

    sns.despine()
    plt.tight_layout()
    plt.savefig(f"time_per_elem_by_size.png", dpi=300, bbox_inches="tight")

    # PLOT #2: time per element by dataset file and key type
    df_results = df_results.sort_values(by="File")
    sns.set_theme(style="white")

    # facet grid to show each data set
    cat = sns.catplot(
        data=df_results, x="Algo", y="TimePerElem", hue="File", col="Field", kind="bar", palette="viridis"
    )
    # move legend off from on top of chart
    sns.move_legend(
        cat, "center left", title="Dataset", frameon=True, edgecolor="lightgray", bbox_to_anchor=(1.02, 0.5)
    )
    cat.set_axis_labels("Algorithm Type", "Time Per Element (microseconds)", fontweight="bold", fontsize=12)
    cat.set_titles('Sort Time per Element by "{col_name}"', fontweight="bold", fontsize=16, pad=25)

    sns.despine()
    plt.tight_layout()
    plt.savefig(f"time_per_elem_by_file_and_key.png", dpi=300, bbox_inches="tight")

    # show visualization
    plt.show()
