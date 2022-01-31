import pytest
from cli import aggregate_words_with_frequency
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def test_no_filepath():
    assert aggregate_words_with_frequency([]) == {}


def test_single_filepath():
    assert aggregate_words_with_frequency([f"{ROOT_DIR}/fixtures/cats_and_mats.txt"]) == {
        "cat": 2,
        "sat": 1,
        "mat": 1
    }


def test_multiple_filepaths():
    assert aggregate_words_with_frequency([f"{ROOT_DIR}/fixtures/cats_and_mats.txt", f"{ROOT_DIR}/fixtures/dogs.txt"]) == {
        "cat": 2,
        "sat": 1,
        "mat": 1,
        "dog": 1,
        "gnawed": 1,
        "bone": 1
    }


def test_duplicate_words():
    assert aggregate_words_with_frequency([f"{ROOT_DIR}/fixtures/cats_and_mats.txt", f"{ROOT_DIR}/fixtures/cats_and_mats.txt"]) == {
        "cat": 4,
        "sat": 2,
        "mat": 2
    }