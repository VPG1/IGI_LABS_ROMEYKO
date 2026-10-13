"""Control work 1: Text analysis, variant 8.
Version: 1.0. Author: Romeiko Matvey Dmitrievich. Date: 2026-10-13.
Purpose: Input validation and execution logging.
"""

from functools import wraps
import logging


def log_execution(function):
    """Log a business function call without exposing its arguments."""
    @wraps(function)
    def wrapper(*args, **kwargs):
        """Preserve the wrapped function result and metadata."""
        logging.info("Starting %s", function.__name__)
        result = function(*args, **kwargs)
        logging.info("Completed %s", function.__name__)
        return result
    return wrapper


def read_integer(prompt, minimum=0, maximum=10000):
    """Read an integer in an inclusive range, retrying invalid input."""
    while True:
        try:
            value = int(input(prompt))
            if not minimum <= value <= maximum:
                raise ValueError("out of range")
            return value
        except ValueError:
            print("Введите целое число от {} до {}.".format(minimum, maximum))


def read_nonempty(prompt):
    """Read a nonempty string, preserving meaningful inner spaces."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Значение не должно быть пустым.")
