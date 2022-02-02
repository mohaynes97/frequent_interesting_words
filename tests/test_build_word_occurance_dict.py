import pytest

from frequent_interesting_words.cli import build_word_occurance_dict


def test_empty_parameters():
    assert build_word_occurance_dict("", ["welp"]) == {}
    assert build_word_occurance_dict("cat on mat", []) == {}


def test_single_word():
    assert build_word_occurance_dict("cat on mat", ["cat"]) == {"cat": 1}


def test_multiple_words():
    assert build_word_occurance_dict("cat on cat on mat", ["cat", "mat"]) == {
        "cat": 2,
        "mat": 1,
    }


def test_test_mixed_case_text():
    assert build_word_occurance_dict("Cat on cat on Mat", ["cat", "mat"]) == {
        "cat": 2,
        "mat": 1,
    }


def test_test_mixed_case_keywords():
    assert build_word_occurance_dict("cat on cat on mat", ["Cat", "Mat"]) == {
        "cat": 2,
        "mat": 1,
    }
