"""Control work 1: Task 2B, Regular expressions, variant 8.
Version: 1.0. Author: Romeiko Matvey Dmitrievich. Date: 2026-10-13.
Purpose: Extract variant-specific results and general text statistics.
"""

from collections import Counter
import re
from utils import log_execution

WORD_PATTERN = re.compile(r"\b\w+\b", re.UNICODE)
UPPER_DIGITS_PATTERN = re.compile(r"\b(?=\w*[A-ZА-ЯЁ])(?=\w*\d)\w+\b")
PASSWORD_PATTERN = re.compile(r"(?=[A-Za-z0-9_]*[A-Z])(?=[A-Za-z0-9_]*[a-z])(?=[A-Za-z0-9_]*[0-9])[A-Za-z0-9_]{8,}")
UPPER_WORD_PATTERN = re.compile(r"[A-ZА-ЯЁ]+")
SMILEY_PATTERN = re.compile(r"(?<![:;])[:;]-*([()\[\]]+)")
SENTENCE_PATTERN = re.compile(r"([^.!?]+)([.!?]+|$)")


def extract_words(text):
    """Return Unicode word tokens containing letters, digits or underscore."""
    return WORD_PATTERN.findall(text)


def words_with_uppercase_and_digits(text):
    """Return every word containing an uppercase Latin/Cyrillic letter and digit."""
    return UPPER_DIGITS_PATTERN.findall(text)


def is_strong_password(password):
    """Check the exact assignment rules using a whole-string regex match."""
    return PASSWORD_PATTERN.fullmatch(password) is not None


def count_uppercase_words(text):
    """Count words consisting entirely of uppercase Latin/Cyrillic letters."""
    return sum(UPPER_WORD_PATTERN.fullmatch(word) is not None
               for word in extract_words(text))


def longest_word_starting_l(text):
    """Return the first longest word starting with Latin l, ignoring case."""
    candidates = [word for word in extract_words(text)
                  if word.casefold().startswith("l")]
    return max(candidates, key=len, default=None)


def repeated_words(text):
    """Return case-insensitive repeated word counts in first-occurrence order."""
    counts = Counter(word.casefold() for word in extract_words(text))
    return {word: count for word, count in counts.items() if count > 1}


def count_smileys(text):
    """Count full bracket runs whose brackets are all identical."""
    return sum(len(set(match.group(1))) == 1
               for match in SMILEY_PATTERN.finditer(text))


def sentence_statistics(text):
    """Compute sentence counts and mean lengths using regex word tokens.

    A sentence must contain a word. A question mark takes precedence over an
    exclamation mark. Exclamations represent the assignment's imperative type;
    an unfinished final sentence is classified as declarative. Spaces and
    punctuation are excluded from character lengths. Abbreviations and decimal
    points are outside this simple punctuation-based segmentation model.
    """
    counts = {"total_sentences": 0, "declarative": 0,
              "interrogative": 0, "imperative": 0}
    word_characters = 0
    word_count = 0
    for match in SENTENCE_PATTERN.finditer(text):
        words = extract_words(match.group(1))
        if not words:
            continue
        punctuation = match.group(2)
        category = ("interrogative" if "?" in punctuation else
                    "imperative" if "!" in punctuation else "declarative")
        counts["total_sentences"] += 1
        counts[category] += 1
        word_count += len(words)
        word_characters += sum(map(len, words))
    counts["avg_sentence_length"] = round(
        word_characters / counts["total_sentences"], 2
    ) if counts["total_sentences"] else 0.0
    counts["avg_word_length"] = round(
        word_characters / word_count, 2
    ) if word_count else 0.0
    counts["smiley_count"] = count_smileys(text)
    return counts


@log_execution
def analyze_text(text, password):
    """Combine every individual and general Task 2B result."""
    return {
        "words_with_uppercase_and_digits": words_with_uppercase_and_digits(text),
        "password_is_strong": is_strong_password(password),
        "uppercase_word_count": count_uppercase_words(text),
        "longest_word_starting_l": longest_word_starting_l(text),
        "repeated_words": repeated_words(text),
        "statistics": sentence_statistics(text),
    }
