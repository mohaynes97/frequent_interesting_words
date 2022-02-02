import pytest
from cli import extract_sample_sentences_from_text


def test_extract_sentence_empty_parameters():
    assert extract_sample_sentences_from_text("mat", "") == []
    assert extract_sample_sentences_from_text("", "cat on mat") == []


def test_extract_single_sentence():
    assert extract_sample_sentences_from_text("good", "Cat on mat. Looks good in hat.") == ["Looks good in hat."]


def test_extract_multiple_sentences():
    assert extract_sample_sentences_from_text("cat", "cat on mat. Looks good in hat. cat loves mat.") == ["cat on mat.", "cat loves mat."]


def test_extract_multiple_sentences_mixed_case():
    assert extract_sample_sentences_from_text("cat", "Cat on mat. cat loves mat.") == ["Cat on mat.", "cat loves mat."]


def test_extract_multiple_sentences_awkward_text_usage():
    assert extract_sample_sentences_from_text("cat", "Cat on mat. cat hates mat..., what!") == ["Cat on mat.", "cat hates mat..., what!"]


def test_extract_sentence_no_substrings():
    assert extract_sample_sentences_from_text("cat", "Catherine loves mats. Cat loves mats.") == ["Cat loves mats."]


def test_extract_sentence_limit():
    assert extract_sample_sentences_from_text("cat", "Cat on mat. Cat loves mat. Cat and mat.", limit=2) == ["Cat on mat.", "Cat loves mat."]