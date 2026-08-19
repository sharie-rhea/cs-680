# Sharie Rhea
# 08.18.26
# SNHU CS680


import os


def main():
    data_dir = "data"

    big_table = {}
    big_total = 0
    for file in os.scandir(data_dir):
        frequency_table = {}
        with open(file, "r") as data:
            # read character by character
            total = 0
            for character in data.read():
                big_total += 1
                total += 1
                if character not in frequency_table:
                    # first occurrence of this character
                    frequency_table[character] = 1
                else:
                    # increment
                    count = frequency_table[character]
                    frequency_table[character] = count + 1
                if character not in big_table:
                    # first occurrence of this character
                    big_table[character] = 1
                else:
                    # increment
                    count = big_table[character]
                    big_table[character] = count + 1

        print(f"number of characters: {len(frequency_table.keys())}")
        sorted_frequencies = dict(sorted(frequency_table.items(), key=lambda item: item[1]))
        for key, value in sorted_frequencies.items():
            print(f"\t{repr(key)}: {value} %: {(value / total) * 100:.4f}")
        print()

    print()
    print(f"number of characters: {len(big_table.keys())}")
    sorted_frequencies = dict(sorted(big_table.items(), key=lambda item: item[1]))
    for key, value in sorted_frequencies.items():
        print(f"\t{repr(key)}: {value} %: {(value / big_total) * 100:.4f}")

    pass


if __name__ == "__main__":
    main()
