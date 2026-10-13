"""Control work 1: Task 2A, Count digits, variant 8.
Version: 1.0. Author: Romeiko Matvey Dmitrievich. Date: 2026-10-13.
Purpose: Count digits in keyboard text without regular expressions.
"""

from utils import log_execution


@log_execution
def count_digits(text):
    """Count characters classified as digits by Unicode str.isdigit."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return sum(character.isdigit() for character in text)
