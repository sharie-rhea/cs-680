# Sharie Rhea
# 08.21.26
# SNHU CS680

import re
import timeit
import unittest
from contextlib import redirect_stdout
from io import StringIO

from App import App


class TestLoadData(unittest.TestCase):
    def setUp(self):
        self.app = App()

    def test_load_valid_data(self):
        """Test loading the provided datasets which are formatted properly by checking that
        the first and last 5 elements are present in the data array."""
        expected1 = [
            "pavonian",
            "befame",
            "conveth",
            "angiemphraxis",
            "piperidine",
            "supersensualistic",
            "squanderingly",
            "clitter",
            "diehard",
            "endoscope",
        ]
        expected2 = [
            "schoolful",
            "Ino",
            "phacopid",
            "audile",
            "paauw",
            "Hyracodontidae",
            "guidance",
            "augitite",
            "Pithecia",
            "grinner",
        ]
        expected3 = [
            "platymesaticephalic",
            "thermoexcitory",
            "unshapen",
            "worky",
            "onshore",
            "Kongo",
            "Sphenodontidae",
            "Tezcatlipoca",
            "agnostic",
            "diarchy",
        ]
        expected4 = [
            "bovine",
            "obscurement",
            "virtuality",
            "fordays",
            "paedomorphism",
            "caddy",
            "untransitory",
            "uncommended",
            "precrucial",
            "trivialize",
        ]
        expected5 = [
            "aerarian",
            "innominatum",
            "graphologic",
            "suitcase",
            "rockelay",
            "psychotherapeutist",
            "patinize",
            "quisquilious",
            "Rhinoderma",
            "smifligate",
        ]

        cases = [
            ("Module 8 Data Set-1.csv", expected1),
            ("Module 8 Data Set-2.csv", expected2),
            ("Module 8 Data Set-3.csv", expected3),
            ("Module 8 Data Set-4.csv", expected4),
            ("Module 8 Data Set-5.csv", expected5),
        ]

        for path, expected in cases:
            with self.subTest(path=path, expected=expected):
                self.app.load_data(path)
                output = self.app.get_data_overview()
                for item in output:
                    self.assertTrue(item in self.app.data)

    def test_missing_file(self):
        """Test loading a file that does not actually exist."""
        with redirect_stdout(StringIO()) as buffer:
            self.app.load_data("missing.csv")
            self.assertEqual(
                "Could not find 'missing.csv', please enter a new dataset path: \n", buffer.getvalue()
            )

    def test_malformed_file(self):
        """Test loading a file that is a csv but does not have the right header fields."""
        with redirect_stdout(StringIO()) as buffer:
            self.app.load_data("malformed.csv")
            self.assertEqual(
                "'malformed.csv' does not adhere to the required dataset format, please enter a new dataset path: \n",
                buffer.getvalue(),
            )

    def test_invalid_file_format(self):
        """Test loading a file that isn't even a csv."""
        with redirect_stdout(StringIO()) as buffer:
            self.app.load_data("image.jpg")
            self.assertEqual(
                "'image.jpg' is not a csv file, please enter a new dataset path: \n", buffer.getvalue()
            )


class TestCreateHeap(unittest.TestCase):

    def setUp(self):
        self.app = App()

    def test_build_heap(self):
        """Test heap creation by viewing the first 5 elements."""
        expected1 = ["Abraham", "Agelaius", "Akhmimic", "Aldus", "Ammonitish"]
        expected2 = ["Aaron", "Aaronic", "Aaronite", "Ab", "Abama"]
        expected3 = ["Aani", "Aaronic", "Aaronical", "Ababdeh", "Abadite"]
        expected4 = ["A", "Aani", "Aaronic", "Aaronite", "Aaronitic"]
        expected5 = ["A", "Aaronic", "Aaronical", "Ababdeh", "Abanic"]

        cases = [
            ("Module 8 Data Set-1.csv", expected1),
            ("Module 8 Data Set-2.csv", expected2),
            ("Module 8 Data Set-3.csv", expected3),
            ("Module 8 Data Set-4.csv", expected4),
            ("Module 8 Data Set-5.csv", expected5),
        ]

        for path, expected in cases:
            with self.subTest(path=path, expected=expected):
                self.app.load_data(path)
                self.app.create_heap()
                output = self.app.get_heap_overview()
                self.assertListEqual(expected, output)


class TestSearch(unittest.TestCase):

    def setUp(self):
        self.app = App()

    def test_valid_search(self):
        """Test searching for a word that does exist in the dataset."""
        expected1 = "unelaborateness"
        expected2 = "vesuvian"
        expected3 = "rafflesiaceous"
        expected4 = "salableness"
        expected5 = "unaroused"

        cases = [
            ("Module 8 Data Set-1.csv", "unelaborateness", expected1),
            ("Module 8 Data Set-2.csv", "vesuvian", expected2),
            ("Module 8 Data Set-3.csv", "rafflesiaceous", expected3),
            ("Module 8 Data Set-4.csv", "salableness", expected4),
            ("Module 8 Data Set-5.csv", "unaroused", expected5),
        ]

        for path, target, expected in cases:
            with self.subTest(path=path, target=target, expected=expected):
                self.app.load_data(path)
                self.app.create_heap()
                output = self.app.search(target)
                self.assertEqual(expected, output[0])

    def test_invalid_search(self):
        """Test searching for a word that does not exist in the dataset."""
        target = "sharie"
        cases = [
            ("Module 8 Data Set-1.csv", target, None),
            ("Module 8 Data Set-2.csv", target, None),
            ("Module 8 Data Set-3.csv", target, None),
            ("Module 8 Data Set-4.csv", target, None),
            ("Module 8 Data Set-5.csv", target, None),
        ]

        for path, target, expected in cases:
            with self.subTest(path=path, target=target, expected=expected):
                self.app.load_data(path)
                self.app.create_heap()
                output = self.app.search(target)
                self.assertEqual(expected, output[0])

    def test_invalid_file_format(self):
        """Test user trying to search for more than one word."""
        with redirect_stdout(StringIO()) as buffer:
            self.app.load_data("Module 8 Data Set-1.csv")
            self.app.create_heap()
            self.assertFalse(self.app.validate_search("two words"))
            self.assertEqual(
                "You may only search for one word at a time, please enter the search target: \n", buffer.getvalue()
            )


class TestRuntime(unittest.TestCase):

    def setUp(self):
        self.app = App()

    def test_valid_search_time(self):
        """Test the time to search for the same valid word using 10 trials."""
        cases = [
            ("Module 8 Data Set-1.csv", "unelaborateness"),
            ("Module 8 Data Set-2.csv", "vesuvian"),
            ("Module 8 Data Set-3.csv", "rafflesiaceous"),
            ("Module 8 Data Set-4.csv", "salableness"),
            ("Module 8 Data Set-5.csv", "unaroused"),
        ]

        for path, target in cases:
            with self.subTest(path=path, target=target):
                self.app.load_data(path)
                self.app.create_heap()
                # make sure the output is correct first
                output = self.app.search(target)
                self.assertEqual(target, output[0])

                # now time it with trials
                result = timeit.timeit(lambda: self.app.search(target), number=10)
                average = result / 10
                print(f"Average time: {average}")
                # assert average time was less than or equal to 20ms
                self.assertGreaterEqual(0.02, average)

    def test_invalid_search_time(self):
        """Test the time to search for the same invalid word using 10 trials."""
        target = "sharie"
        cases = [
            ("Module 8 Data Set-1.csv", target),
            ("Module 8 Data Set-2.csv", target),
            ("Module 8 Data Set-3.csv", target),
            ("Module 8 Data Set-4.csv", target),
            ("Module 8 Data Set-5.csv", target),
        ]

        for path, target in cases:
            with self.subTest(path=path, target=target):
                self.app.load_data(path)
                self.app.create_heap()
                # make sure the output is correct first
                output = self.app.search(target)
                self.assertEqual(None, output[0])

                # now time it with trials
                result = timeit.timeit(lambda: self.app.search(target), number=10)
                average = result / 10
                print(f"Average time: {average}")
                # assert average time was less than or equal to 40ms
                self.assertGreaterEqual(0.04, average)


class TestFormat(unittest.TestCase):

    def setUp(self):
        self.app = App()

    def test_opening_prompt(self):
        """Test the opening app prompt."""

        expected = """--- STRAT DATA DATASET SEARCH APP ---
Please enter a dataset path to get started (exit to quit): 
"""

        with redirect_stdout(StringIO()) as buffer:
            self.app.display_greeting()
            self.assertEqual(expected, buffer.getvalue())

    # test that only data field is shown, records searched are shown, data field is labeled
    def test_search_prompt(self):
        """Test the search prompt."""

        expected = "Please enter the target word (exit to quit): \n"
        with redirect_stdout(StringIO()) as buffer:
            self.app.prompt_search()
            self.assertEqual(expected, buffer.getvalue())

    def test_valid_search_output(self):
        """Test that valid output is properly formatted."""

        expected1 = """- RESULTS -
\trecords searched: x
\tdata: unelaborateness
"""
        expected2 = """- RESULTS -
\trecords searched: x
\tdata: vesuvian
"""
        expected3 = """- RESULTS -
\trecords searched: x
\tdata: rafflesiaceous
"""
        expected4 = """- RESULTS -
\trecords searched: x
\tdata: salableness
"""
        expected5 = """- RESULTS -
\trecords searched: x
\tdata: unaroused
"""

        cases = [
            ("Module 8 Data Set-1.csv", "unelaborateness", expected1),
            ("Module 8 Data Set-2.csv", "vesuvian", expected2),
            ("Module 8 Data Set-3.csv", "rafflesiaceous", expected3),
            ("Module 8 Data Set-4.csv", "salableness", expected4),
            ("Module 8 Data Set-5.csv", "unaroused", expected5),
        ]

        for path, target, expected in cases:
            with self.subTest(path=path, target=target, expected=expected):
                self.app.load_data(path)
                self.app.create_heap()
                with redirect_stdout(StringIO()) as buffer:
                    result, num_searched = self.app.search(target)
                    # replace the number of records searched with x, because we are
                    # not verifying this by hand, although it should be deterministic
                    self.app.display_result(result, num_searched)
                    buffer = re.sub("[0-9]+", "x", buffer.getvalue())
                    self.assertEqual(expected, buffer)

    def test_invalid_search_output(self):
        target = "sharie"
        expected = """- RESULTS -
\trecords searched: x
\tNo match found!
"""

        cases = [
            ("Module 8 Data Set-1.csv", target, expected),
            ("Module 8 Data Set-2.csv", target, expected),
            ("Module 8 Data Set-3.csv", target, expected),
            ("Module 8 Data Set-4.csv", target, expected),
            (
                "Module 8 Data Set-5.csv",
                target,
                expected,
            ),
        ]

        for path, target, expected in cases:
            with self.subTest(path=path, target=target, expected=expected):
                self.app.load_data(path)
                self.app.create_heap()
                with redirect_stdout(StringIO()) as buffer:
                    result, num_searched = self.app.search(target)
                    # replace the number of records searched with x, because we are
                    # not verifying this by hand, although it should be deterministic
                    self.app.display_result(result, num_searched)
                    buffer = re.sub("[0-9]+", "x", buffer.getvalue())
                    self.assertEqual(expected, buffer)

    def test_shutdown_output(self):
        with self.assertRaises(SystemExit):
            expected = "Thank you! Exiting...\n"
            with redirect_stdout(StringIO()) as buffer:
                self.app.display_shutdown()
                self.assertEqual(expected, buffer.getvalue())


if __name__ == "__main__":
    # run in verbose mode to show the names of each test that is run
    unittest.main(verbosity=2)
