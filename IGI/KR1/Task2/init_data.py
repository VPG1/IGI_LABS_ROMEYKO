"""Control work 1: Text analysis, variant 8.
Version: 1.0. Author: Romeiko Matvey Dmitrievich. Date: 2026-10-13.
Purpose: Initialize a caller-provided sequence using input or a generator.
"""

import random
import string


def init_from_input(sequence, count, reader=input):
    """Replace sequence contents with count strings entered by the user."""
    if not isinstance(count, int) or not 1 <= count <= 10000:
        raise ValueError("count must be an integer between 1 and 10000")
    sequence[:] = [reader("Строка {}: ".format(i + 1)) for i in range(count)]
    return sequence


def generate_lines(count, length=24, seed=None):
    """Yield random text lines from letters, decimal digits and spaces."""
    if not isinstance(count, int) or not 1 <= count <= 10000:
        raise ValueError("count must be an integer between 1 and 10000")
    if not isinstance(length, int) or not 1 <= length <= 10000:
        raise ValueError("length must be an integer between 1 and 10000")
    random_source = random.Random(seed)
    alphabet = string.ascii_letters + string.digits + "     "
    for _ in range(count):
        yield "".join(random_source.choice(alphabet) for _ in range(length))


def init_from_generator(sequence, count, length=24, seed=None):
    """Replace sequence contents using an actual generator function."""
    sequence[:] = list(generate_lines(count, length, seed))
    return sequence
