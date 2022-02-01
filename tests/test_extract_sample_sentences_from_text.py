import pytest
from cli import extract_sample_sentences_from_text


def test_extract_sentence_empty_text():
    assert extract_sample_sentences_from_text("mat", "") == ""