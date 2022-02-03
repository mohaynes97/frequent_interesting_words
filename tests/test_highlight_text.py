import pytest

from frequent_interesting_words.cli import highlight_text


def test_highlight_no_input():
    assert highlight_text("", "word") == ""
    assert highlight_text("text", "") == "text"


def test_highlight_word():
    assert highlight_text("cat on mat.", "cat") == "**cat** on mat."


def test_highlight_word_mixed_case():
    assert (
        highlight_text("Cat on mat with cat.", "cat") == "**Cat** on mat with **cat**."
    )


def test_highlight_apostraphe_esque_special_cases():
    assert (
        highlight_text("cat's on mat, cat`s on mat, cat’s on mat.", "cat")
        == "**cat's** on mat, **cat`s** on mat, **cat’s** on mat."
    )
