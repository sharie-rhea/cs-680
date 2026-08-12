import collections
import csv
import os
import random
import timeit

from avl_tree import AVLTree


def load_data(file_path) -> list:
    print(f"Loading file {file_path}...")
    try:
        with open(file_path, newline="") as file:
            reader = csv.DictReader(file, delimiter="|")
            # just return a list of the data, no need to keep sequence num
            data = []
            for row in reader:
                data.append(row["data"])
            return data
    except Exception as e:
        raise Exception(f"Error: unable to load file {file_path}: {e}")


def search_and_display(tree: AVLTree, target):
    """Helper method to call in the Timer that also displays some info."""
    node = tree.search(target)
    if not node:
        print(f"\t{target} not found in tree!")
        return

    print(f"\t{target} found! Count: {node.count} Height: {node.height}")


def time_trials(filename, avl_tree, items, duplicates) -> list[dict]:
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


def run_analysis() -> list[dict]:
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

    return results


def main():
    # NOTE: uncomment to re-run analysis
    # results: list[dict] = run_analysis()
    # fieldnames = results[0].keys()
    # with open("analysis_results2.csv", "w") as file:
    #     writer = csv.DictWriter(file, fieldnames)
    #     writer.writeheader()
    #     for row in results:
    #         writer.writerow(row)

    data = []
    try:
        with open("analysis_results2.csv", newline="") as file:
            reader = csv.DictReader(file, delimiter=",")
            for row in reader:
                data.append(row)
    except Exception as e:
        raise Exception(f"Error: unable to load file analysis_results2.csv: {e}")

    # convert times to microseconds (and to a float not string)
    for row in data:
        row["AvgTime_µs"] = float(row["AvgTime"]) * 1_000_000

    # calculate time by dataset size and category
    # I know this is really ugly... standard library only, no pandas

    # note that size is parsed as a string, no real need to convert though
    times = [row["AvgTime_µs"] for row in data if row["Size"] == "1000" and row["Category"] == "random"]
    avg_1000_random = sum(times) / len(times)
    times = [row["AvgTime_µs"] for row in data if row["Size"] == "1000" and row["Category"] == "duplicate"]
    avg_1000_duplicate = sum(times) / len(times)
    times = [row["AvgTime_µs"] for row in data if row["Size"] == "1000" and row["Category"] == "not present"]
    avg_1000_not_present = sum(times) / len(times)

    times = [row["AvgTime_µs"] for row in data if row["Size"] == "100000" and row["Category"] == "random"]
    avg_100000_random = sum(times) / len(times)
    times = [row["AvgTime_µs"] for row in data if row["Size"] == "100000" and row["Category"] == "duplicate"]
    avg_100000_duplicate = sum(times) / len(times)
    times = [row["AvgTime_µs"] for row in data if row["Size"] == "100000" and row["Category"] == "not present"]
    avg_100000_not_present = sum(times) / len(times)

    times = [row["AvgTime_µs"] for row in data if row["Size"] == "401000" and row["Category"] == "random"]
    avg_40100_random = sum(times) / len(times)
    times = [row["AvgTime_µs"] for row in data if row["Size"] == "401000" and row["Category"] == "duplicate"]
    avg_40100_duplicate = sum(times) / len(times)
    times = [row["AvgTime_µs"] for row in data if row["Size"] == "401000" and row["Category"] == "not present"]
    avg_40100_not_present = sum(times) / len(times)

    # display results
    print()
    print()
    print()
    print("--- RESULTS ---")
    print("Average Time for 1000 elements:")
    print(f"\tRandom:      {avg_1000_random:.4}µs")
    print(f"\tDuplicate:   {avg_1000_duplicate:.4}µs")
    print(f"\tNot present: {avg_1000_not_present:.4}µs")
    print()
    print("Average Time for 100,000 elements:")
    print(f"\tRandom:      {avg_100000_random:.4}µs")
    print(f"\tDuplicate:   {avg_100000_duplicate:.4}µs")
    print(f"\tNot present: {avg_100000_not_present:.4}µs")
    print()
    print("Average Time for 401,000 elements:")
    print(f"\tRandom:      {avg_40100_random:.4}µs")
    print(f"\tDuplicate:   {avg_40100_duplicate:.4}µs")
    print(f"\tNot present: {avg_40100_not_present:.4}µs")

    """
    If you wish to create plots for the measured results, read the csv file using pandas
    to create a dataframe, then import matplotlib, pandas, and seaborn. Uncomment this
    section to enable plotting!


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
    """


if __name__ == "__main__":
    main()
