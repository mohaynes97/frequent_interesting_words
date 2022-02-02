import pytest
from cli import build_interesting_word_frequency_dict


def test_missing_parameters():
    assert build_interesting_word_frequency_dict("", "welp", 10) == {}
    assert build_interesting_word_frequency_dict("text", "", 10) == {}


def test_text():
    data = build_interesting_word_frequency_dict(
        "cat sat on mat with another cat", "/test/cats_and_mats.txt", 10
    )

    assert list(data.keys()) == ["cat", "sat", "mat"]
    for word, v in data.items():
        for file, frequency in v.items():
            assert file == "/test/cats_and_mats.txt"
            assert frequency == 2 if word == "cat" else frequency == 1
