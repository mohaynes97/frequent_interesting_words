import pytest

from frequent_interesting_words.cli import highlight_text


def test_highlight_no_input():
    assert highlight_text("", "word") == ""
    assert highlight_text("text", "") == "text"


def test_highlight_word():
    assert highlight_text("cat on mat.", "cat") == "**cat** on mat."


def test_highlight_apostraphe():
    assert (
        highlight_text("cat's on mat with cat.", "cat")
        == "**cat's** on mat with **cat**."
    )
