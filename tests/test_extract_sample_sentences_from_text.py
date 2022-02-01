import pytest
from cli import extract_sample_sentences_from_text


def test_extract_sentence_empty_parameters():
    assert extract_sample_sentences_from_text("mat", "") == []
    assert extract_sample_sentences_from_text("", "cat on mat") == []
