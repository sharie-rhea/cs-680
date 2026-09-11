# Sharie Rhea
# 08.21.26
# SNHU CS680
import csv
import heapq
from typing import Optional


class App:
    data: list = []

    def display_greeting(self) -> None:
        print("--- STRAT DATA DATASET SEARCH APP ---")
        print("Please enter a dataset path to get started (exit to quit): ")

    def run(self) -> None:
        self.display_greeting()
        is_data_valid = False
        while not is_data_valid:
            path = self.get_input()
            is_data_valid = self.load_data(path)

        self.create_heap()

        # continue to allow searches forever
        while True:
            self.prompt_search()
            target = self.get_input()

            # error handle trying to search for more than one word
            while not self.validate_search(target):
                target = self.get_input()

            print(f"Searching for '{target}'...")
            result, num_searched = self.search(target)
            self.display_result(result, num_searched)

    def validate_search(self, target) -> bool:
        if len(target.split(" ")) > 1:
            print("You may only search for one word at a time, please enter the search target: ")
            return False
        return True

    def load_data(self, path: str) -> bool:
        # error handle improper file type
        if not path.endswith(".csv"):
            print(f"'{path}' is not a csv file, please enter a new dataset path: ")
            return False

        # use a set to remove duplicate values
        temp = set()
        try:
            with open(path, "r") as file:
                reader = csv.DictReader(file, delimiter="|")
                # error handle invalid headings
                if reader.fieldnames != ["sequence", "data"]:
                    print(f"'{path}' does not adhere to the required dataset format, please enter a new dataset path: ")
                    return False

                # if we reached this point, file is valid, now just need to collect data
                for row in reader:
                    # ignore empty string values
                    if row["data"] != "":
                        temp.add(row["data"])
            # convert to list for later heapify
            self.data = list(temp)
            return True
        except FileNotFoundError:
            # error handle missing file
            print(f"Could not find '{path}', please enter a new dataset path: ")
            return False

    def get_data_overview(self) -> list[str]:
        # get first 5 elements and last 5 elements from loaded data
        return self.data[:5] + self.data[-5:]

    def create_heap(self):
        self.heap = self.data
        heapq.heapify(self.heap)

    def get_heap_overview(self) -> list[str]:
        # get first 5 elements in heap
        return_val = []
        for i in range(0, 5):
            return_val.append(heapq.heappop(self.heap))

        # put the items back in so we don't modify the data
        for item in return_val:
            heapq.heappush(self.heap, item)
        return return_val

    def get_input(self) -> str:
        value = input()
        if value.lower() == "exit":
            self.display_shutdown()
        return value

    def prompt_search(self) -> None:
        print("Please enter the target word (exit to quit): ")

    def search(self, target) -> tuple[Optional[str], int]:
        # data is stored in a min-heap, using DFS to search
        # left child is always 2i + 1, right child is always 2i + 2
        # if we hit a node that is greater than what we are searching for, no need to continue this path,
        # all further elements are too great

        heap = self.heap
        heap_len = len(heap)
        if not heap_len:
            return (None, 0)

        # stack for iterative implementation
        stack = [0]
        num_searched = 0

        while stack:
            index = stack.pop()
            num_searched += 1
            value = heap[index]

            # is this our target?
            if value == target:
                return (target, num_searched)

            # can we short-circuit because this element is too great?
            if value < target:
                left = (index << 1) + 1
                # check bounds before pushing onto stack to avoid useless iterations
                # also, if left is out of bound, then no need to check right
                if left < heap_len:
                    stack.append(left)
                    if left + 1 < heap_len:
                        stack.append(left + 1)

        return (None, num_searched)

    def display_result(self, result, num_searched) -> None:
        print("- RESULTS -")
        print(f"\trecords searched: {num_searched}")
        if not result:
            print("\tNo match found!")
        else:
            print(f"\tdata: {result}")

    def display_shutdown(self) -> None:
        print("Thank you! Exiting...")
        exit()

if __name__ == "__main__":
    app = App()
    app.run()
