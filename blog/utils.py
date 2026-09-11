import math
import re


def calculate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """
    Calculate estimated reading time in minutes for a given text.
    Standard average reading speed is ~200 words per minute.
    Returns a minimum of 1 minute.
    """
    if not text or not text.strip():
        return 1
    # Match alphanumeric words, ignoring punctuation
    words = re.findall(r'\b\w+\b', text)
    word_count = len(words)
    minutes = math.ceil(word_count / words_per_minute)
    return max(1, minutes)
