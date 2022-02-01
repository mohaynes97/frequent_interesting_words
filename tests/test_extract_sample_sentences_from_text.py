import pytest
from cli import extract_sample_sentences_from_text


def test_extract_sentence_empty_parameters():
    assert extract_sample_sentences_from_text("mat", "") == []
    assert extract_sample_sentences_from_text("", "cat on mat") == []


def test_extract_single_sentence():
    assert extract_sample_sentences_from_text("good", "Cat on mat. Looks good in hat.") == ["Looks good in hat."]