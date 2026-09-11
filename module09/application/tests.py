# Sharie Rhea
# 08.26.26
# SNHU CS680

import filecmp
import os
import re
import timeit
import unittest
from contextlib import redirect_stdout
from io import StringIO

from App import App
from DataHandler import DataHandler
from HuffmanCoding import HuffmanCoding

DATASET_FILEPATHS = [
    "CS 680 Project Data Set-1.csv",
    "CS 680 Project Data Set-2.csv",
    "CS 680 Project Data Set-3.csv",
    "CS 680 Project Data Set-4.csv",
]


class TestLoadData(unittest.TestCase):
    """Performance of reading the original data set."""

    def test_load_valid_data(self):
        """Test loading the provided datasets and checking number of rows."""
        expected = [1000, 100000, 100000, 100000]

        cases = zip(DATASET_FILEPATHS, expected)
        for path, expected_output in cases:
            with self.subTest(path=path, expected_output=expected_output):
                dataset = DataHandler(path)
                output = dataset.load_row_list()
                self.assertEqual(expected_output, output)

    def test_missing_file(self):
        """Test attempting to read a missing file."""
        with redirect_stdout(StringIO()) as buffer:
            DataHandler("missing.csv")
            self.assertEqual("\tCould not find 'missing.csv'!\n", buffer.getvalue())

    def test_malformed_file(self):
        """Test attempting to read a malformed file (invalid field headings)."""
        with redirect_stdout(StringIO()) as buffer:
            dataset = DataHandler("malformed.csv")
            dataset.load_row_list()
            self.assertEqual(
                "\t'malformed.csv' does not adhere to the required dataset format!\n",
                buffer.getvalue(),
            )

    def test_build_row_list(self):
        """Test loading the provided datasets (which are formatted properly) by checking presence of a few values."""

        # expected is the first and last values in the dataset file
        expected = [
            # set 1
            [
                (
                    "0",
                    "112109",
                    "71",
                    "6",
                    "coachability nepenthe venomy recusancy frontierman repression ballproof",
                    "c3a97fd9bd45c9e99c60dacc3220327d56f232b83626023ed76c8b8be725e06c",
                ),
                (
                    "999",
                    "512426",
                    "60",
                    "5",
                    "jointweed expugn sesquiquadrate hepatical Ji hypsometrically",
                    "f31c4b0db2858361f103106ed85cfbed3b24c80a507d91ff429c8a8fcb1454b0",
                ),
            ],
            # set 2
            [
                (
                    "0",
                    "844878",
                    "39",
                    "3",
                    "resigner Acrasida subsidency swinebread",
                    "c122aa9191a8528393026421c3f2484d007932161e09d872c256bbb2ad5cc9d4",
                ),
                (
                    "99999",
                    "406330",
                    "69",
                    "6",
                    "octobass gladly sharpen Olenellus traditionary pronative palladammine",
                    "33c88bb12526a5e3bbfc1f772c41cbc9c64572d6af98c794a51740fa632171dc",
                ),
            ],
            # set 3
            [
                (
                    "0",
                    "455137",
                    "67",
                    "5",
                    "paramorphine incumbency hyoglossal peristaphyline untellable rumple",
                    "1c7b17706d2c518dd5a02e81b0e257bf47f1f02ced65942f8dfd42b21f8fa42c",
                ),
                (
                    "99999",
                    "149378",
                    "53",
                    "4",
                    "facular parviflorous presumedly rootless unshrivelled",
                    "d0739e516cd1203431e266e8c3f29882239503eb0aa4daca33c1bbcf46ba443c",
                ),
            ],
            # set 4
            [
                (
                    "0",
                    "541649",
                    "43",
                    "3",
                    "Compsothlypidae Saussurea ropewalker Aselli",
                    "769f0beb0ee048e0ad1d3fd7251e2742f41b7a0203c25143b50e493caed6d17f",
                ),
                (
                    "99999",
                    "742033",
                    "40",
                    "3",
                    "trifledom mediatress outweep gardenesque",
                    "c5ef4ddee3517914c0d02e85bb9043f01a7f4f319aea5ed3411c2fafc7c2d6ad",
                ),
            ],
        ]

        cases = zip(DATASET_FILEPATHS, expected)
        for path, expected_output in cases:
            with self.subTest(path=path, expected_output=expected_output):
                dataset = DataHandler(path)
                dataset.load_row_list()
                for item in expected_output:
                    self.assertTrue(item in dataset.row_list)

    def test_load_data_runtime(self):
        """Test the runtime for the create the row list."""
        # 60ms, 600ms
        expected = [0.06, 0.6, 0.6, 0.6]

        cases = zip(DATASET_FILEPATHS, expected)
        for path, target in cases:
            with self.subTest(path=path, target=target):
                dataset = DataHandler(path)
                result = timeit.timeit(lambda: dataset.load_row_list(), number=3)
                average = result / 3
                print(f"[TIME] Average time load_data {path}: {average}")
                # assert average time is at least as good as the target
                self.assertGreaterEqual(target, average)


class TestHuffmanTree(unittest.TestCase):
    """Validity of Huffman tree construction using small example data."""

    def setUp(self) -> None:
        self.dataset = DataHandler(path=DATASET_FILEPATHS[0])
        self.coding = HuffmanCoding(contents=self.dataset.raw_data)

    def test_single_character(self):
        """Test the edge case where there is only one symbol."""
        coding = HuffmanCoding(contents="aaaaa")
        codes = coding.get_codes()
        self.assertEqual(len(codes), 1)
        self.assertIn("a", codes)
        self.assertEqual("0", codes["a"])

    def test_root_weight(self):
        """Test that the weight of the root node is equal to total character count."""
        self.assertEqual(self.coding.root.weight, len(self.dataset.raw_data))

    def test_total_nodes(self):
        """Test that total nodes are 2k - 1 for alphabet size k."""
        k = len(set(self.dataset.raw_data))
        total_nodes = self.coding.get_total_node_count()
        self.assertEqual(2 * k - 1, total_nodes)

    def test_prefix_free(self):
        """Test to make sure that all codes follw the prefix free property."""
        code_values = list(self.coding.get_codes().values())

        # compare each and every code against each other
        for i, code1 in enumerate(code_values):
            for j, code2 in enumerate(code_values):
                if i != j:
                    self.assertFalse(code2.startswith(code1))

    def test_build_huffman_tree_runtime(self):
        """Test the runtime for constructing the tree."""
        expected = [0.02, 1.0, 1.0, 1.0]

        cases = zip(DATASET_FILEPATHS, expected)
        for path, target in cases:
            with self.subTest(path=path, target=target):
                dataset = DataHandler(path)
                result = timeit.timeit(lambda: HuffmanCoding(contents=dataset.raw_data), number=3)
                average = result / 3
                print(f"[TIME] Average time construct tree {path}: {average}")
                # assert average time is at least as fast as the target
                self.assertGreaterEqual(target, average)


class TestWriteCompressed(unittest.TestCase):
    """Performance of writing the compressed data set."""

    def setUp(self):
        self.app = App()

    def test_write_compressed(self):
        """Test that writing compressed data creates a non-empty file."""
        for path in DATASET_FILEPATHS:
            output = path.replace(".csv", "_compressed.csv")
            with self.subTest(path=path):
                self.assertTrue(os.path.isfile(output))
                self.assertTrue(os.stat(output).st_size != 0)

    def test_compress_runtime(self):
        """Test the runtime for compressing the data."""
        expected = [0.1, 8, 8, 8]

        cases = zip(DATASET_FILEPATHS, expected)
        for path, target in cases:
            with self.subTest(path=path, target=target):
                dataset = DataHandler(path)
                result = timeit.timeit(lambda: dataset.compress(), number=3)
                average = result / 3
                print(f"[TIME] Average time compress data {path}: {average}")
                # assert average time
                self.assertGreaterEqual(target, average)

    def test_write_compressed_runtime(self):
        """Test the runtime for writing the compressed data."""
        expected = [0.005, 0.02, 0.02, 0.02]

        cases = zip(DATASET_FILEPATHS, expected)
        for path, target in cases:
            with self.subTest(path=path, target=target):
                dataset = DataHandler(path)
                dataset.compress()
                result = timeit.timeit(lambda: dataset.write_out_compressed(), number=3)
                average = result / 3
                print(f"[TIME] Average time write compressed {path}: {average}")
                # assert average time
                self.assertGreaterEqual(target, average)


class TestReadCompressed(unittest.TestCase):
    """Performance of reading the compressed data set."""

    def setUp(self):
        self.app = App()

    def test_read_compressed_runtime(self):
        """Test the runtime for reading the compressed data."""
        expected = [0.02, 0.5, 0.5, 0.5]

        cases = zip(DATASET_FILEPATHS, expected)
        for path, target in cases:
            with self.subTest(path=path, target=target):
                dataset = DataHandler(path)
                dataset.compressed_path = path.replace(".csv", "_compressed.bin")
                result = timeit.timeit(lambda: dataset.read_compressed(), number=3)
                average = result / 3
                print(f"[TIME] Average time read compressed {path}: {average}")
                # assert average time
                self.assertGreaterEqual(target, average)

    def test_decompress_runtime(self):
        """Test the runtime for decompressing the data."""
        expected = [0.5, 27, 27, 27]

        cases = zip(DATASET_FILEPATHS, expected)
        for path, target in cases:
            with self.subTest(path=path, target=target):
                dataset = DataHandler(path)
                dataset.compressed_path = path.replace(".csv", "_compressed.bin")
                data = dataset.read_compressed()
                result = timeit.timeit(lambda: dataset.decompress(data), number=3)
                average = result / 3
                print(f"[TIME] Average time decompress {path}: {average}")
                # assert average time
                self.assertGreaterEqual(target, average)


class TestWriteDecompressed(unittest.TestCase):
    """Performance of writing the uncompressed data set."""

    def setUp(self):
        self.dataset = DataHandler("CS 680 Project Data Set-1.csv")
        self.dataset.decompress(self.dataset.compress())

    def test_write_decompressed(self):
        """Test that writing uncompressed data creates a non-empty file."""
        output = self.dataset.write_out_decompressed()
        self.assertTrue(os.path.isfile(output))
        self.assertTrue(os.stat(output).st_size != 0)

    def test_write_decompressed_runtime(self):
        """Test the runtime for writing the uncompressed data."""
        expected = [0.005, 0.1, 0.1, 0.1]

        cases = zip(DATASET_FILEPATHS, expected)
        for path, target in cases:
            with self.subTest(path=path, target=target):
                path = path.replace(".csv", "_decompressed.csv")
                dataset = DataHandler(path)
                dataset.decompressed = dataset.raw_data
                result = timeit.timeit(lambda: dataset.write_out_decompressed(), number=3)
                average = result / 3
                print(f"[TIME] Average time write uncompressed {path}: {average}")
                # assert average time
                self.assertGreaterEqual(target, average)


class TestCompressedIntegrity(unittest.TestCase):
    """Comparison of the uncompressed data set to the original data set."""

    def test_compression_integrity_external(self):
        for path in DATASET_FILEPATHS:
            dataset = DataHandler(path)
            dataset.decompress(dataset.compress())
            decompressed_path = dataset.write_out_decompressed()
            # compare file sizes first
            self.assertEqual(os.stat(path).st_size, os.stat(decompressed_path).st_size)
            # compare contents
            self.assertTrue(filecmp.cmp(path, decompressed_path, shallow=False))


class TestComplexity(unittest.TestCase):
    """Algorithmic complexity of the solution."""

    def setUp(self):
        self.app = App()

    def test_compression_scaling_filesize(self):
        """Test how much the file size was compressed."""
        # expect at least 30% compression
        expected = [30, 30, 30, 30]

        cases = zip(DATASET_FILEPATHS, expected)
        for path, expected_out in cases:
            with self.subTest(path=path, expected_out=expected_out):
                original_size = os.stat(path).st_size
                dataset = DataHandler(path)
                dataset.compress()
                compressed_path = dataset.write_out_compressed()
                compressed_size = os.stat(compressed_path).st_size

                compression = 100 - (compressed_size / original_size * 100)
                print(f"[COMPRESSION] {path}: {compression}%")
                self.assertLessEqual(expected_out, compression)

    def test_tree_build_scaling_runtime(self):
        """Test growth scales near O(N) or O(N log N) rather than quadratic O(N^2)."""
        # compare the smaller dataset to one of the larger ones
        small_dataset = DataHandler(DATASET_FILEPATHS[0])
        large_dataset = DataHandler(DATASET_FILEPATHS[1])

        t_small = timeit.timeit(lambda: HuffmanCoding(contents=small_dataset.raw_data), number=3) / 3
        # this one is 100x larger
        t_large = timeit.timeit(lambda: HuffmanCoding(contents=large_dataset.raw_data), number=3) / 3

        scale = t_large / t_small
        print(f"\n[COMPLEXITY] 1k vs 100k n | Scale increase: {scale:.2f}x")

        # make sure that we are definitely scaling less than n^2
        self.assertLess(scale, 10000)
        # make sure we are scaling less than n log n
        self.assertLess(scale, 200)


if __name__ == "__main__":
    # set up the compressed and decompressed datasets for some of the read/write tests so we
    # aren't doing a bunch of unnecessary compression and decompression

    print("Setting up compressed and decompressed files...")
    for path in DATASET_FILEPATHS:
        print(f"\t{path}...")
        dataset = DataHandler(path)
        compressed = dataset.compress()
        dataset.write_out_compressed()
        dataset.decompress(compressed)
        dataset.write_out_decompressed()

    # run in verbose mode to show the names of each test that is run
    unittest.main(verbosity=2)
