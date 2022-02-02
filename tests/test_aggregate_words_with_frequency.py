import pytest
from cli import aggregate_words_with_frequency
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture
def cats_and_mats_data():
    return {
        "cat": {"cats_and_mats": 2},
        "sat": {"cats_and_mats": 1},
        "mat": {"cats_and_mats": 1}
    }


@pytest.fixture
def dogs_data():
    return {
        "dog": {"dogs": 1},
        "gnawed": {"dogs": 1},
        "bone": {"dogs": 1}
    }


@pytest.fixture
def dog_and_cat_data():
    return {
        "dog": {"dog_and_cat": 1},
        "cat": {"dog_and_cat": 1},
    }


def test_no_data():
    assert aggregate_words_with_frequency([]) == {}


def test_single_dict(cats_and_mats_data):
    assert aggregate_words_with_frequency([cats_and_mats_data]) == cats_and_mats_data


def test_multiple_filepaths(cats_and_mats_data, dogs_data):
    assert aggregate_words_with_frequency([cats_and_mats_data, dogs_data]) == {
        "cat": { "cats_and_mats": 2 },
        "sat": { "cats_and_mats": 1 },
        "mat": { "cats_and_mats": 1 },
        "dog": { "dogs": 1 },
        "gnawed": { "dogs": 1 },
        "bone": { "dogs": 1 }
    }


def test_filepaths_with_overlapping_words(cats_and_mats_data, dog_and_cat_data):
    assert aggregate_words_with_frequency([cats_and_mats_data, dog_and_cat_data]) == {
        "cat": { "cats_and_mats": 2, "dog_and_cat": 1 },
        "sat": { "cats_and_mats": 1 },
        "mat": { "cats_and_mats": 1 },
        "dog": { "dog_and_cat": 1 },
    }


def test_duplicate_paths_override(cats_and_mats_data):
    assert aggregate_words_with_frequency([cats_and_mats_data, cats_and_mats_data]) == {
        "cat": { "cats_and_mats": 2 },
        "sat": { "cats_and_mats": 1 },
        "mat": { "cats_and_mats": 1 },
    }