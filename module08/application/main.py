import csv
import re
from contextlib import redirect_stdout
from io import StringIO

from App import App


def test():
    with open("data/set5.csv", "r") as file:
        reader = csv.DictReader(file, delimiter="|")
        values = []
        for row in reader:
            values.append(row["data"])

        values.sort()

        for i in range(0, 6):
            print(values[i])


app = App()
app.load_data(input())
app.create_heap()
print(app.get_data_overview())
