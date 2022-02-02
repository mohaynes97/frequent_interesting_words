import pytest

from cli import extract_keywords


@pytest.fixture
def extracted_keywords_lower_case():
    return [
        ("a", 0.1),
        ("b", 0.2),
        ("c", 0.54),
        ("d", 0.71),
        ("e", 0.32),
        ("f", 0.45),
        ("g", 0.61),
        ("h", 0.85),
        ("i", 0.99),
        ("j", 1),
    ]


@pytest.fixture
def extracted_keywords_mixed_case():
    return [
        ("A", 0.1),
        ("b", 0.2),
        ("c", 0.54),
        ("D", 0.71),
        ("e", 0.32),
        ("f", 0.45),
        ("G", 0.61),
        ("h", 0.85),
        ("i", 0.99),
        ("j", 1),
    ]


@pytest.fixture
def extractor_mock(mocker):
    def func(keywords):
        mock_extractor = mocker.MagicMock()
        mock_extractor.configure_mock(**{"extract_keywords.return_value": keywords})
        return mock_extractor

    return func


def test_extract_keyword_empty_text():
    assert extract_keywords("", 10) == []


def test_extract_keyword_simple():
    assert extract_keywords("cat on mat", 10) == ["cat", "mat"]


def test_extract_keyword_limit():
    assert extract_keywords("cat on mat with cat and ant", 2) == ["ant", "cat"]


def test_extract_keyword_ordered(mocker, extractor_mock, extracted_keywords_lower_case):
    mock = extractor_mock(extracted_keywords_lower_case)
    mocker.patch("yake.KeywordExtractor", return_value=mock)
    assert extract_keywords("irrelevant", 10) == [
        "a",
        "b",
        "e",
        "f",
        "c",
        "g",
        "d",
        "h",
        "i",
        "j",
    ]
    mock.extract_keywords.assert_called_once_with("irrelevant")


def test_extract_keyword_lower_case(
    mocker, extractor_mock, extracted_keywords_mixed_case
):
    mock = extractor_mock(extracted_keywords_mixed_case)
    mocker.patch("yake.KeywordExtractor", return_value=mock)
    assert extract_keywords("irrelevant", 10) == [
        "a",
        "b",
        "e",
        "f",
        "c",
        "g",
        "d",
        "h",
        "i",
        "j",
    ]
    mock.extract_keywords.assert_called_once_with("irrelevant")
