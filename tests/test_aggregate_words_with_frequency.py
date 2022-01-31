import pytest
from cli import aggregate_words_with_frequency
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def test_no_filepath():
    assert aggregate_words_with_frequency([]) == {}


def test_single_filepath():
    assert aggregate_words_with_frequency([f"{ROOT_DIR}/fixtures/cats_and_mats.txt"]) == {
        "cat": {
            "cats_and_mats": 2
        },
        "sat": {
            "cats_and_mats": 1
        },
        "mat": {
            "cats_and_mats": 1
        }
    }


def test_multiple_filepaths():
    assert aggregate_words_with_frequency([f"{ROOT_DIR}/fixtures/cats_and_mats.txt", f"{ROOT_DIR}/fixtures/dogs.txt"]) == {
        "cat": {
            "cats_and_mats": 2
        },
        "sat": {
            "cats_and_mats": 1
        },
        "mat": {
            "cats_and_mats": 1
        },
        "dog": {
            "dogs": 1
        },
        "gnawed": {
            "dogs": 1
        },
        "bone": {
            "dogs": 1
        }
    }


def test_filepaths_with_overlapping_words():
    assert aggregate_words_with_frequency([f"{ROOT_DIR}/fixtures/cats_and_mats.txt", f"{ROOT_DIR}/fixtures/dog_and_cat.txt"]) == {
        "cat": {
            "cats_and_mats": 2,
            "dog_and_cat": 1
        },
        "sat": {
            "cats_and_mats": 1
        },
        "mat": {
            "cats_and_mats": 1
        },
        "dog": {
            "dog_and_cat": 1
        },
    }


def test_duplicate_paths():
    assert aggregate_words_with_frequency([f"{ROOT_DIR}/fixtures/cats_and_mats.txt", f"{ROOT_DIR}/fixtures/cats_and_mats.txt"]) == {
        "cat": {
            "cats_and_mats": 2
        },
        "sat": {
            "cats_and_mats": 1
        },
        "mat": {
            "cats_and_mats": 1
        }
    }