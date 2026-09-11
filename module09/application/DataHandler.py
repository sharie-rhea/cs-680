import csv
import os

from HuffmanCoding import BitReader, HuffmanCoding

# static fieldnames for the defined dataset format
FIELDNAMES = ["index", "value", "clen", "ws", "data", "validation"]


class DataHandler:
    """Manager for loading, saving, compressing, and decompressing dataset files."""

    def __init__(self, path: str, contents: str | None = None):
        # if the path is a csv file, grab the filename to use as a prefix
        prefix = path[:-4] if path.lower().endswith(".csv") else path
        self.path = path
        # set up file names for the compressed and decompressed versions
        self.compressed_path = f"{prefix}_compressed.bin"
        self.decompressed_path = f"{prefix}_decompressed.csv"

        # load data (if contents are not provided directly)
        self.raw_data = contents if contents is not None else self.load_raw_data()

    def load_raw_data(self) -> str:
        """Load raw text data from the csv path."""
        if not self.path.endswith(".csv"):
            print(f"\t'{self.path}' is not a csv file!")
            return ""
        try:
            with open(self.path, "r") as file:
                self.raw_data = file.read()
                return self.raw_data
        except FileNotFoundError:
            print(f"\tCould not find '{self.path}'!")
            return ""

    def load_row_list(self) -> int:
        """Parse raw string data into a list of tuple records. Returns count of valid records."""
        # make sure data was loaded
        if not self.raw_data:
            self.load_raw_data()

        reader = csv.DictReader(self.raw_data.splitlines(), delimiter="|")
        if reader.fieldnames != FIELDNAMES:
            print(f"\t'{self.path}' does not adhere to the required dataset format!")
            return -1

        # data is valid, get records
        self.row_list = [tuple(row[f] for f in FIELDNAMES) for row in reader]
        return len(self.row_list)

    def compress(self) -> bytearray:
        """Compress raw text using Huffman coding into binary structure."""
        coding = HuffmanCoding(contents=self.raw_data)
        tree_bytes, tree_pad = coding.encode_tree()
        payload_bytes, payload_pad = coding.encode_contents()

        # pack it all together
        # format is: [tree len:2][tree_pad:1][payload_pad:1][payload:variable length]
        self.compressed_data = bytearray(
            len(tree_bytes).to_bytes(2, "big") + bytes([tree_pad, payload_pad]) + tree_bytes + payload_bytes
        )
        return self.compressed_data

    def decompress(self, data_bytes: bytearray) -> str:
        """Decompress binary data, returning the string representation."""
        # format is: [tree len:2][tree_pad:1][payload_pad:1][payload:variable length]

        # parse length information from the 4 header bytes
        tree_len = int.from_bytes(data_bytes[:2], "big")
        tree_pad, payload_pad = data_bytes[2], data_bytes[3]

        # reconstruct the tree
        tree_reader = BitReader(data_bytes[4 : 4 + tree_len], padding_amount=tree_pad)
        coding = HuffmanCoding.decode_tree(tree_reader)

        # it's way to slow to follow pointers for each bit of data
        # create a nested tuple structure instead (left, right)
        root = coding.tree_to_tuples(coding.root)

        payload_bytes = data_bytes[4 + tree_len :]
        total_payload_bits = (len(payload_bytes) * 8) - payload_pad

        out = []
        # local variable lookups are faster
        out_append = out.append
        curr = root
        bits_processed = 0

        for byte in payload_bytes:
            # shift to read from MSB to LSB
            for shift in (7, 6, 5, 4, 3, 2, 1, 0):
                if bits_processed >= total_payload_bits:
                    break

                bit = (byte >> shift) & 1
                # index left or right in the tuple
                curr = curr[bit]

                # landed on a string which means a leaf node -> end of this codword
                if type(curr) is str:
                    out_append(curr)
                    # reset for next decoding
                    curr = root  # Reset to root

                bits_processed += 1

        self.decompressed = "".join(out)
        return self.decompressed

    def write_out_decompressed(self) -> str:
        """Write out the decompressed data to a file."""
        with open(self.decompressed_path, "w", encoding="utf-8") as f:
            f.write(self.decompressed)
        return self.decompressed_path

    def write_out_compressed(self) -> str:
        """Write out the compressed binary data to a file."""
        with open(self.compressed_path, "wb") as f:
            f.write(self.compressed_data)
        return self.compressed_path

    def read_compressed(self) -> bytearray:
        """Read the compressed binary data from a file."""
        with open(self.compressed_path, "rb") as f:
            return bytearray(f.read())

    def print_compression_stats(self) -> None:
        """Display original size vs compressed size and the compression percentage."""
        og_size = os.stat(self.path).st_size / 1000
        comp_size = os.stat(self.compressed_path).st_size / 1000
        percent = 100 - (comp_size / og_size * 100) if og_size else 0

        print(f"\t\tOriginal size  : {og_size:.2f}KB")
        print(f"\t\tCompressed size: {comp_size:.2f}KB")
        print(f"\t\tCompression    : {percent:.2f}%")
