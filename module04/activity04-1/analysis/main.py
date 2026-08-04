import collections
import os
import random
import timeit

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from avl_tree import AVLTree
from matplotlib.container import BarContainer


def load_data(file_path) -> list:
    print(f"Loading file {file_path}...")
    # keep_default_na=False handles blank strings
    df = pd.read_csv(file_path, sep="|", keep_default_na=False)
    # just return a list of the data, no need to keep sequence num
    return list(df["data"])


def search_and_display(tree: AVLTree, target):
    """Helper method to call in the Timer that also displays some info."""
    node = tree.search(target)
    if not node:
        print(f"\t{target} not found in tree!")
        return

    print(f"\t{target} found! Count: {node.count} Height: {node.height}")


def time_trials(filename, avl_tree, items, duplicates):
    results = []
    trials = 10
    n = len(items)
    # time trials for searching a random element
    target = random.choice(items)
    print(f"\tSearching for {target}...")
    # NOTE: uncomment to print extra info, but adds time to the tests
    # timer = timeit.Timer(lambda: search_and_display(tree, target))
    timer = timeit.Timer(lambda: avl_tree.search(target))

    total_time = timer.timeit(number=trials)
    avg_time = total_time / trials
    time_per_elem = avg_time / n
    results.append(
        {
            "File": filename,
            "AvgTime": avg_time,
            "Size": n,
            "AvgTime": avg_time,
            "TimePerElem": time_per_elem,
            "Category": "random",
        }
    )

    # time trials for searching an element that has duplicates
    target = random.choice(duplicates)
    print(f"\tSearching for {target}...")
    # NOTE: uncomment to print extra info, but adds time to the tests
    # timer = timeit.Timer(lambda: search_and_display(tree, target))
    timer = timeit.Timer(lambda: avl_tree.search(target))

    total_time = timer.timeit(number=trials)
    avg_time = total_time / trials
    time_per_elem = avg_time / n
    results.append(
        {
            "File": filename,
            "AvgTime": avg_time,
            "Size": n,
            "AvgTime": avg_time,
            "TimePerElem": time_per_elem,
            "Category": "duplicate",
        }
    )

    # time trials for searching an element that is not in the tree
    target = "sharie"
    print(f"\tSearching for {target}...")
    # NOTE: uncomment to print extra info, but adds time to the tests
    # timer = timeit.Timer(lambda: search_and_display(tree, target))
    timer = timeit.Timer(lambda: avl_tree.search(target))

    total_time = timer.timeit(number=trials)
    avg_time = total_time / trials
    time_per_elem = avg_time / n
    results.append(
        {
            "File": filename,
            "AvgTime": avg_time,
            "Size": n,
            "AvgTime": avg_time,
            "TimePerElem": time_per_elem,
            "Category": "not present",
        }
    )

    return results


def run_analysis() -> pd.DataFrame:
    results = []
    data_dir = "data"
    combined_data = []

    for file in os.scandir(data_dir):
        # load the data and build the AVL tree
        items = load_data(file.path)
        combined_data += items
        avl_tree: AVLTree = AVLTree.build_tree_from_list(items)

        # figure out which values have duplicates
        counter = collections.Counter(items)
        duplicates = [key for key, value in counter.items() if value > 1]
        results += time_trials(file.name, avl_tree, items, duplicates)

        # DEBUG: printing to check order and height
        # print("AVL tree:")
        # print("In order: ")
        # avl_tree.print_in_order()
        # print("Preorder: ")
        # avl_tree.print_preorder()
        # print(avl_tree.height(avl_tree.root))

    # also check with ALL the data combined into one large dataset
    avl_tree: AVLTree = AVLTree.build_tree_from_list(combined_data)
    # figure out which values have duplicates
    counter = collections.Counter(combined_data)
    duplicates = [key for key, value in counter.items() if value > 1]
    results += time_trials("combined data", avl_tree, combined_data, duplicates)

    return pd.DataFrame(results)


def main():
    # NOTE: uncomment to re-run analysis
    # df_results = run_analysis()
    # df_results.to_csv("analysis_results.csv")

    # plotting for analysis!
    df_results = pd.read_csv("analysis_results.csv")
    # convert times to microseconds
    df_results["AvgTime"] = df_results["AvgTime"] * 1_000_000

    # PLOT #1: time per element by dataset size
    sns.set_theme(style="white")
    # create the figure
    plt.figure(figsize=(10, 6))
    chart = sns.barplot(data=df_results, x="Size", y="AvgTime", hue="Category", palette="viridis", errorbar=None)

    # add numeric labels above bars
    for container in chart.containers:
        assert isinstance(container, BarContainer)
        chart.bar_label(container, fmt="%.1f", padding=3, fontsize=10)

    # title and axis labels
    plt.title("Binary Search on AVL Tree: Average Time by Dataset Size", fontsize=16, fontweight="bold", pad=25)
    plt.xlabel("Dataset Size (n)", fontsize=12, fontweight="bold")
    plt.ylabel("Average Time (µs)", fontsize=12, fontweight="bold")

    sns.despine()
    plt.tight_layout()
    plt.savefig(f"time_by_size.png", dpi=300, bbox_inches="tight")

    plt.show()


if __name__ == "__main__":
    main()
