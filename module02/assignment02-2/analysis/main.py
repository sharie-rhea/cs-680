# Sharie Rhea
# 07.17.26
# SNHU CS680

import copy
import os
import random
import timeit

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from algorithms import (
    binary_search,
    binary_search_linked_list,
    binary_search_tree,
    insertionsort,
    insertionsort_linked_list,
    insertionsort_tree,
)
from binary_tree import build_tree, print_in_order
from linked_list import build_linked_list


def load_data(file_path):
    print(f"Loading file {file_path}...")
    # keep_default_na=False handles blank strings
    df = pd.read_csv(file_path, sep="|", keep_default_na=False)
    # convert to a list of dicts for easier sorting
    dictionary = df.to_dict("records")


# comparators that return -1/0/1
def comp_key(node_data, target):
    if node_data["key"] == target["key"]:
        return 0
    return -1 if target["key"] < node_data["key"] else 1


def comp_data(node_data, target):
    if node_data["data"] == target["data"]:
        return 0
    return -1 if target["data"] < node_data["data"] else 1


def run_analysis():
    results = []
    data_dir = "data"
    trials = 3

    for file in os.scandir(data_dir):
        rows = load_data(file.path)
        n = len(rows)

        # rows is our "array" implementation, now build linked list and tree
        linked_head = build_linked_list(rows)
        tree_head_key = build_tree(rows, comp_key)
        tree_head_data = build_tree(rows, comp_data)

        # DEBUG: uncomment to check that tree is sorted
        # print_in_order(tree_head_key)

        fields = {"key": comp_key, "data": comp_data}
        name = "Insertion Sort"
        # time insertion sort on array
        print("Beginning insertion sort on array...")
        for field, comp in fields.items():
            # cap insertion sort to 1000 elements
            timer = timeit.Timer(lambda: insertionsort(rows[:1000], comp))
            total_time = timer.timeit(number=trials)
            avg_time = total_time / trials
            time_per_elem = avg_time / n
            results.append(
                {
                    "File": file.name,
                    "AvgTime": avg_time,
                    "Size": 1000,
                    "Algo": name,
                    "Field": field,
                    "AvgTime": avg_time,
                    "TimePerElem": time_per_elem,
                    "DataStructure": "array",
                }
            )
        # on linked list
        print("Beginning insertion sort on linked list...")
        for field, comp in fields.items():
            # cap insertion sort at 1000
            head = build_linked_list(rows[:1000])
            timer = timeit.Timer(lambda: insertionsort_linked_list(head, comp))
            total_time = timer.timeit(number=trials)
            avg_time = total_time / trials
            time_per_elem = avg_time / n
            results.append(
                {
                    "File": file.name,
                    "AvgTime": avg_time,
                    "Size": 1000,
                    "Algo": name,
                    "Field": field,
                    "AvgTime": avg_time,
                    "TimePerElem": time_per_elem,
                    "DataStructure": "linked list",
                }
            )
        # no example for insertion sort on binary tree, doesn't really make sense

        name = "Binary Search"
        # pick a random target to search for
        target = random.choice(rows)
        # time binary search on array
        print(f"Beginning binary search for {target} on array...")
        for field, comp in fields.items():
            rows.sort(key=lambda d: d[field])
            timer = timeit.Timer(lambda: binary_search(rows, target, comp))
            total_time = timer.timeit(number=trials)
            avg_time = total_time / trials
            time_per_elem = avg_time / n
            results.append(
                {
                    "File": file.name,
                    "AvgTime": avg_time,
                    "Size": n,
                    "Algo": name,
                    "Field": field,
                    "AvgTime": avg_time,
                    "TimePerElem": time_per_elem,
                    "DataStructure": "array",
                }
            )
        # on linked list
        print(f"Beginning binary search for {target} on linked list...")
        for field, comp in fields.items():
            rows.sort(key=lambda d: d[field])
            linked_sorted = build_linked_list(rows)
            timer = timeit.Timer(lambda: binary_search_linked_list(linked_sorted, target, comp))
            total_time = timer.timeit(number=trials)
            avg_time = total_time / trials
            time_per_elem = avg_time / n
            results.append(
                {
                    "File": file.name,
                    "AvgTime": avg_time,
                    "Size": n,
                    "Algo": name,
                    "Field": field,
                    "AvgTime": avg_time,
                    "TimePerElem": time_per_elem,
                    "DataStructure": "linked list",
                }
            )
        # on tree
        print(f"Beginning binary search for {target} on tree...")
        for field, comp in fields.items():
            head = tree_head_key if field == "key" else tree_head_data
            timer = timeit.Timer(lambda: binary_search_tree(head, target, comp))
            total_time = timer.timeit(number=trials)
            avg_time = total_time / trials
            time_per_elem = avg_time / n
            results.append(
                {
                    "File": file.name,
                    "AvgTime": avg_time,
                    "Size": n,
                    "Algo": name,
                    "Field": field,
                    "AvgTime": avg_time,
                    "TimePerElem": time_per_elem,
                    "DataStructure": "tree",
                }
            )

        name = "Binary Search (target not found)"
        # pick a non-existent target
        target = {"key": 123456789, "data": "sharie rhea", "validation": ""}
        # time binary search on array
        print(f"Beginning binary search for {target} on array...")
        for field, comp in fields.items():
            rows.sort(key=lambda d: d[field])
            timer = timeit.Timer(lambda: binary_search(rows, target, comp))
            total_time = timer.timeit(number=trials)
            avg_time = total_time / trials
            time_per_elem = avg_time / n
            results.append(
                {
                    "File": file.name,
                    "AvgTime": avg_time,
                    "Size": n,
                    "Algo": name,
                    "Field": field,
                    "AvgTime": avg_time,
                    "TimePerElem": time_per_elem,
                    "DataStructure": "array",
                }
            )
        # on linked list
        print(f"Beginning binary search for {target} on linked list...")
        for field, comp in fields.items():
            rows.sort(key=lambda d: d[field])
            linked_sorted = build_linked_list(rows)
            timer = timeit.Timer(lambda: binary_search_linked_list(linked_sorted, target, comp))
            total_time = timer.timeit(number=trials)
            avg_time = total_time / trials
            time_per_elem = avg_time / n
            results.append(
                {
                    "File": file.name,
                    "AvgTime": avg_time,
                    "Size": n,
                    "Algo": name,
                    "Field": field,
                    "AvgTime": avg_time,
                    "TimePerElem": time_per_elem,
                    "DataStructure": "linked list",
                }
            )
        # on tree
        print(f"Beginning binary search for {target} on tree...")
        for field, comp in fields.items():
            head = tree_head_key if field == "key" else tree_head_data
            timer = timeit.Timer(lambda: binary_search_tree(head, target, comp))
            total_time = timer.timeit(number=trials)
            avg_time = total_time / trials
            time_per_elem = avg_time / n
            results.append(
                {
                    "File": file.name,
                    "AvgTime": avg_time,
                    "Size": n,
                    "Algo": name,
                    "Field": field,
                    "AvgTime": avg_time,
                    "TimePerElem": time_per_elem,
                    "DataStructure": "tree",
                }
            )

    return pd.DataFrame(results)


if __name__ == "__main__":
    # NOTE: uncomment to re-run analysis
    # df_results = run_analysis()
    # df_results.to_csv("analysis_results.csv")

    # plotting for analysis!
    # PLOT 1: by dataset
    df_results = pd.read_csv("analysis_results.csv")
    df_results = df_results.sort_values(by="File")
    # convert times to microseconds
    df_results["TimePerElem"] = df_results["TimePerElem"] * 1e9

    sns.set_theme(style="white")

    binary_search_df = df_results[df_results["Algo"] != "Insertion Sort"]
    plt.figure(figsize=(10, 6))
    chart = sns.barplot(
        data=binary_search_df, x="File", y="TimePerElem", hue="DataStructure", palette="viridis", errorbar=None
    )

    # add numeric labels above bars
    for container in chart.containers:
        chart.bar_label(container, fmt="%.1f", padding=3, fontsize=10)

    # move legend off from on top of chart
    sns.move_legend(
        chart, "center left", title="Dataset", frameon=True, edgecolor="lightgray", bbox_to_anchor=(1.02, 0.5)
    )

    # title and axis labels
    plt.title("Binary Search: Average Time per Element by Data Set", fontsize=16, fontweight="bold", pad=25)
    plt.xlabel("File", fontsize=12, fontweight="bold")
    plt.ylabel("Average Time per Element (ns)", fontsize=12, fontweight="bold")
    plt.yscale("log")

    sns.despine()
    plt.tight_layout()
    plt.savefig(f"binary_search_by_file.png", dpi=300, bbox_inches="tight")

    # PLOT 2: by existence of target
    binary_search_df = df_results[df_results["Algo"] != "Insertion Sort"]
    plt.figure(figsize=(10, 6))
    chart = sns.barplot(
        data=binary_search_df, x="Algo", y="TimePerElem", hue="DataStructure", palette="viridis", errorbar=None
    )

    # add numeric labels above bars
    for container in chart.containers:
        chart.bar_label(container, fmt="%.1f", padding=3, fontsize=10)

    # move legend off from on top of chart
    sns.move_legend(
        chart, "center left", title="Dataset", frameon=True, edgecolor="lightgray", bbox_to_anchor=(1.02, 0.5)
    )

    # title and axis labels
    plt.title("Binary Search: Average Time per Element by Target Existence", fontsize=16, fontweight="bold", pad=25)
    plt.xlabel("Existence of Target", fontsize=12, fontweight="bold")
    plt.ylabel("Average Time per Element (ns)", fontsize=12, fontweight="bold")
    plt.yscale("log")

    sns.despine()
    plt.tight_layout()
    plt.savefig(f"binary_search_by_target.png", dpi=300, bbox_inches="tight")


    plt.show()
