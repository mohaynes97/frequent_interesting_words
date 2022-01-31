import pytest
from cli import aggregate_words_with_frequency


def test_no_filepath():
    assert aggregate_words_with_frequency([]) == {}


def test_single_filepath():
    assert aggregate_words_with_frequency(["test_docs/cats_and_mats.txt"]) == {
        "cat": 2,
        "sat": 1,
        "mat": 1
    }