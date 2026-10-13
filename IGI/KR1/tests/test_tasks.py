"""Control work 1: Independent checks for variant 8.
Version: 1.0. Author: Romeiko Matvey Dmitrievich. Date: 2026-10-13.
Purpose: Check required behavior, edge cases, files and geometric invariants.
"""

import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "Task2"), str(ROOT / "Task4")]
import matplotlib
matplotlib.use("Agg")
from task2a import count_digits
from task2b import (words_with_uppercase_and_digits, is_strong_password,
                    count_uppercase_words, longest_word_starting_l,
                    repeated_words, count_smileys, sentence_statistics)
from init_data import init_from_input, init_from_generator
from file_io import analyze_file
from abstract_figure import GeometricFigure
from figure_color import FigureColor
from pentagon import RegularPentagon


class TextTests(unittest.TestCase):
    """Check examples and boundaries independently of implementation details."""

    def test_digits(self):
        """Count digits including zeros and Unicode digit characters."""
        for text, expected in [("", 0), ("abc", 0), ("Вариант 8, 2026", 5),
                               ("0123456789", 10), ("١٢²", 3)]:
            with self.subTest(text=text):
                self.assertEqual(count_digits(text), expected)

    def test_digit_type(self):
        """Reject a non-string instead of silently converting it."""
        with self.assertRaises(TypeError):
            count_digits(8)

    def test_upper_and_digits(self):
        """Require both conditions and preserve complete word tokens."""
        self.assertEqual(words_with_uppercase_and_digits("A12 abc1 HELLO C00l_Pass Р2 123"),
                         ["A12", "C00l_Pass", "Р2"])

    def test_valid_passwords(self):
        """Accept both assignment examples and an eight-character boundary."""
        for password in ["C00l_Pass", "SupperPas1", "Aa123456"]:
            with self.subTest(password=password):
                self.assertTrue(is_strong_password(password))

    def test_invalid_passwords(self):
        """Reject missing categories, forbidden characters and trailing newlines."""
        for password in ["Cool_pass", "C00l", "AAAAAAA1", "abcdefg1", "Abcdefgh",
                         "Пароль123A", "Abcd1234!", "Abcd1234\n", "", " Abcd1234"]:
            with self.subTest(password=password):
                self.assertFalse(is_strong_password(password))

    def test_uppercase_words(self):
        """Exclude mixed case, numeric words and underscores."""
        self.assertEqual(count_uppercase_words("HELLO РОБОТ Hello A12 123 A_B"), 2)

    def test_longest_l(self):
        """Return the first longest candidate and handle an absent candidate."""
        self.assertEqual(longest_word_starting_l("lamp laboratory long"), "laboratory")
        self.assertIsNone(longest_word_starting_l("дом text"))

    def test_repeated_words(self):
        """Ignore capitalization and strip punctuation during tokenization."""
        self.assertEqual(repeated_words("Hello, hello! мир Мир world"), {"hello": 2, "мир": 2})

    def test_valid_smileys(self):
        """Accept all four bracket kinds with arbitrary minus counts."""
        self.assertEqual(count_smileys(":) ;---[[[ :--((( ;]]"), 4)

    def test_invalid_smileys(self):
        """Reject absent brackets, repeated prefixes and mixed bracket runs."""
        self.assertEqual(count_smileys("] ;-- : ) :)( ::) ;-[)"), 0)

    def test_sentence_statistics(self):
        """Check manually counted word characters and punctuation categories."""
        self.assertEqual(sentence_statistics("Hello world. Why? Go!"), {
            "total_sentences": 3, "declarative": 1, "interrogative": 1,
            "imperative": 1, "avg_sentence_length": 5.0,
            "avg_word_length": 3.75, "smiley_count": 0})

    def test_empty_statistics(self):
        """Avoid division by zero and exclude punctuation-only sentences."""
        stats = sentence_statistics("...?! :)")
        self.assertEqual(stats["total_sentences"], 0)
        self.assertEqual(stats["avg_sentence_length"], 0.0)
        self.assertEqual(stats["smiley_count"], 1)

    def test_unfinished_and_combined_punctuation(self):
        """Count an unfinished tail and classify a mixed ending as a question."""
        stats = sentence_statistics("Really?! Tail")
        self.assertEqual(stats["total_sentences"], 2)
        self.assertEqual(stats["interrogative"], 1)
        self.assertEqual(stats["declarative"], 1)

    def test_input_initialization(self):
        """Initialize the same supplied sequence from deterministic user values."""
        sequence = ["old"]
        values = iter(["A1", "B2"])
        self.assertIs(init_from_input(sequence, 2, lambda prompt: next(values)), sequence)
        self.assertEqual(sequence, ["A1", "B2"])

    def test_generator_initialization(self):
        """Honor count and line length and reproduce a supplied random seed."""
        first, second = [], []
        init_from_generator(first, 3, 12, 8)
        init_from_generator(second, 3, 12, 8)
        self.assertEqual(first, second)
        self.assertEqual(list(map(len, first)), [12, 12, 12])

    def test_invalid_generator_count(self):
        """Reject an invalid sequence dimension."""
        with self.assertRaises(ValueError):
            init_from_generator([], 0)

    def test_file_archive_workflow(self):
        """Read a BOM, preserve UTF-8 output and verify ZIP bytes and metadata."""
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory)/"input.txt", Path(directory)/"result.txt"
            source.write_text("\ufeffHELLO A1 laboratory. :) HELLO!", encoding="utf-8")
            results, metadata = analyze_file(source, output, "C00l_Pass")
            self.assertEqual(results["repeated_words"], {"hello": 2})
            with zipfile.ZipFile(output.with_suffix(".zip")) as archive:
                self.assertIsNone(archive.testzip())
                self.assertEqual(archive.read("result.txt"), output.read_bytes())
            self.assertEqual(metadata["size"], len(output.read_bytes()))
            self.assertEqual(json.loads(output.with_suffix(".json").read_text()), results)

    def test_protect_input_file(self):
        """Prevent overwriting the source with the report."""
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)/"input.txt"
            source.write_text("Original", encoding="utf-8")
            with self.assertRaises(ValueError):
                analyze_file(source, source, "")
            self.assertEqual(source.read_text(), "Original")


class GeometryTests(unittest.TestCase):
    """Check shape invariants and required OOP behavior."""

    def test_abstract_class(self):
        """Ensure the base figure cannot be instantiated."""
        with self.assertRaises(TypeError):
            GeometricFigure()

    def test_pentagon_area(self):
        """Check a independently tabulated area for side five."""
        self.assertAlmostEqual(RegularPentagon(5, "blue").calculate_area(), 43.0119350147, places=9)

    def test_five_equal_sides(self):
        """Check that every adjacent vertex pair has the requested side."""
        points = RegularPentagon(5, "blue").vertices()
        self.assertEqual(len(points), 5)
        for first, second in zip(points, points[1:]+points[:1]):
            self.assertAlmostEqual(math.dist(first, second), 5, places=10)

    def test_shoelace_area(self):
        """Compare analytic area against the independent polygon formula."""
        pentagon = RegularPentagon(7, "#23A6C8")
        points = pentagon.vertices()
        cross_sum = sum(x1*y2-x2*y1 for (x1,y1),(x2,y2)
                        in zip(points, points[1:]+points[:1]))
        self.assertAlmostEqual(abs(cross_sum)/2, pentagon.calculate_area(), places=10)

    def test_invalid_sides(self):
        """Reject zero, negatives, infinity, NaN and nonnumeric data."""
        for side in [0, -1, float("inf"), float("nan"), "abc", True]:
            with self.subTest(side=side), self.assertRaises(ValueError):
                RegularPentagon(side, "blue")

    def test_color_property(self):
        """Accept a changed valid color and reject an invalid replacement."""
        color = FigureColor("blue")
        color.color = "#23A6C8"
        self.assertEqual(color.color, "#23A6C8")
        for invalid in ["", "not-a-color", "none"]:
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                color.color = invalid

    def test_name_and_description(self):
        """Return the class name and the required parameters."""
        pentagon = RegularPentagon(5, "blue")
        self.assertEqual(pentagon.get_name(), "Правильный пятиугольник")
        for fragment in ["a = 5", "blue", "43.011935"]:
            self.assertIn(fragment, pentagon.describe())

    def test_save_figure(self):
        """Save an actual nonempty PNG without a GUI window."""
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/"pentagon.png"
            RegularPentagon(5, "skyblue").draw("Вариант 8", output, show=False)
            self.assertGreater(output.stat().st_size, 1000)
            self.assertEqual(output.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
