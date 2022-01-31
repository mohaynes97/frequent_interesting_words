import pytest
from cli import extract_words_with_frequecy_from_file


def test_bad_filepath():
    with pytest.raises(FileNotFoundError):
        extract_words_with_frequecy_from_file("/this/cannot/exist/de(ar/heavens/let/this/not/exist")


def test_empty_file():
    assert extract_words_with_frequecy_from_file("test_docs/empty.txt") == {}


def test_extract_words_with_frequency():
      assert extract_words_with_frequecy_from_file("test_docs/cats_and_mats.txt") == {
        "cat": 2,
        "sat": 1,
        "mat": 1
    }