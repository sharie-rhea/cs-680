# Sharie Rhea
# 09.05.26
# SNHU CS680

import filecmp
import os

from DataHandler import DataHandler


class App:

    def main_loop(self):
        """The main application loop that interacts with the user."""
        print("--- ACME NEURAL INTELLIGENCE DATA COMPRESSION APP ---")
        print("Enter 'exit' at any time to quit.")

        while True:
            # dataset input and loading
            path = self.get_input("Please enter a dataset path to get started: ")
            dataset = DataHandler(path)
            print(f"\tLoading records from {path}...")
            num_records = dataset.load_row_list()
            if num_records == -1:
                continue
            print(f"\tSuccessfully loaded {num_records} records!")
            print()

            # compress and write out
            print(f"\tStarting Huffman compression...")
            dataset.compress()
            print(f"\tCompression complete!")
            dataset.write_out_compressed()
            dataset.print_compression_stats()
            print()
            print(f"\tData written to {dataset.compressed_path}.")
            print()

            # read compressed data back in
            print(f"\tReading compressed data back in...")
            raw_compressed = dataset.read_compressed()
            print(f"\tDecompressing...")
            decoded = dataset.decompress(raw_compressed)
            print(f"\tDecompression complete!")
            dataset.write_out_decompressed()
            print(f"\tData written to {dataset.decompressed_path}.")
            print()

            # compare data integrity
            print(f"\tChecking that original and decompressed sizes match...")
            if os.stat(dataset.path).st_size == os.stat(dataset.decompressed_path).st_size:
                print(f"\tSuccess! Checking contents...")
                if filecmp.cmp(dataset.path, dataset.decompressed_path, shallow=False):
                    print(f"\tSuccess! Integrity checks out.")
                else:
                    print(f"\tERROR: files have different contents!")
            else:
                print(f"\tERROR: sizes do not match!")
            print()

    def shutdown(self):
        """Cleanly exit the application."""
        print("Thank you! Exiting...")
        exit(0)

    def get_input(self, prompt: str) -> str:
        """Helper method to handle exiting at any input."""
        value = input(prompt)
        if value.lower() == "exit":
            self.shutdown()
        return value

if __name__ == "__main__":
    app = App()
    app.main_loop()
