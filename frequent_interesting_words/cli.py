import os
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Type, TypedDict

import click
import nltk
import yake
from pytablewriter import MarkdownTableWriter
from yake.highlight import TextHighlighter

import re


class WordsWithFrequencyDict(TypedDict):
    word: str
    doc_path_to_frequency_map: dict[str, int]


def extract_keywords(text: str, word_limit: int) -> list[str]:
    """
    Build a list of important words from a given piece of text

    Args:
        text: text to extract keywords from
        word_limit: limits the keywords extracted to the x most important

    Returns: list of lower case keywords in the text sorted in frequency order
    """
    kw_extractor = yake.KeywordExtractor(
        lan="en", n=1, dedupLim=0.9, top=word_limit, features=None
    )
    keywords = kw_extractor.extract_keywords(text)

    return [k[0].lower() for k in sorted(keywords, key=lambda x: x[1])]


def build_word_occurance_dict(text: str, words: Iterable[str]) -> dict[str, int]:
    """
    Build a dictionary of the frequency of words contained within a body of text

    Args:
        text: text in which the frequency of words will be checked
        words: words to check the frequency of

    Returns: Dict mapping words to its frequency in the text
    """
    all_words = nltk.tokenize.word_tokenize(text)
    stopwords = nltk.corpus.stopwords.words("english")
    lower_case_words = [k.lower() for k in words]
    filtered_words = nltk.FreqDist(
        w.lower()
        for w in all_words
        if w not in stopwords and w.lower() in lower_case_words
    )

    return filtered_words


def build_interesting_word_frequency_dict(
    text: str, path: str, word_limit: int
) -> WordsWithFrequencyDict:
    """
    Build a WordsWithFrequencyDict from a piece of text

    Args:
        text: the text to build the WordsWithFrequencyDict from
        path: the filepath to the doc which contains the text
        word_limit: the upper limit of keywords to extract from the text

    Returns:
        A WordsWithFrequencyDict
    """
    if not path or not text:
        return {}

    return {
        word: {path: frequency}
        for word, frequency in build_word_occurance_dict(
            text, extract_keywords(text, word_limit)
        ).items()
    }


def flatten_and_sort_words_with_frequency(
    words_with_frequency: WordsWithFrequencyDict,
) -> list[tuple[str, int]]:
    """
    Flattens a WordsWithFrequencyDict into a list of tuples, these being
    pairs of (word, frequency), also sorts them

    Args:
        words_with_frequency: WordsWithFrequencyDict to flatten and sort

    Returns:
        list of tuples of (word, frequency)
    """
    flattened_words = [
        (k, sum(frequency for _, frequency in v.items()))
        for k, v in words_with_frequency.items()
    ]
    # ordered by frequency, followed by alphabetical
    return sorted(flattened_words, key=lambda x: (-x[1], x[0]))


def aggregate_words_with_frequency(
    interesting_word_frequency_collection: Iterable[WordsWithFrequencyDict],
    limit: int = None,
) -> WordsWithFrequencyDict:
    """
    Do a deep merge on a collecion of WordsWithFrequencyDicts to combine them into a single one

    Args:
        interesting_word_frequency_collection: Iterable of WordWithFrequencyDicts to merge
        limit: An upper limit in the total number of words in the final WordsWithFrequencyDict

    Returns: A WordsWithFrequencyDict that is the aggregation of those in the collection
    """
    result = defaultdict(dict)
    for interesting_word_frequency_dict in interesting_word_frequency_collection:
        for word, v in interesting_word_frequency_dict.items():
            for document, frequency in v.items():
                result[word][document] = frequency

    if limit:
        result = {
            k: v
            for k, v in result.items()
            if k
            in [x for x, _ in flatten_and_sort_words_with_frequency(result)[:limit]]
        }
    return result


def extract_sample_sentences_from_text(
    keyword: str, text: str, limit: int = None
) -> list[str]:
    """
    Pulls a number of sample sentences from the text based on the keyword

    Args:
        keyword: Sentences are pulled fro the text if they contain this word
        text: text to pull sentences from
        limit: upper bound on the number of sentences to extract, falsy means unlimited

    Returns: List of sentences extracted from the text
    """
    if not keyword or not text:
        return []

    sentences = nltk.tokenize.sent_tokenize(text)
    sample_sentences = [
        sentence
        for sentence in sentences
        if keyword.lower() in nltk.tokenize.word_tokenize(sentence.lower())
    ]
    if limit:
        sample_sentences = sample_sentences[:limit]
    return sample_sentences


def highlight_text(text: str, word: str) -> str:
    """Highlight the given word within the text using md bold syntax"""
    return TextHighlighter(
        max_ngram_size=1, highlight_pre="**", highlight_post="**"
    ).highlight(text, [word, f"{word}’s", f"{word}'s", f"{word}`s"])


def format_output_table(
    words_with_frequency: WordsWithFrequencyDict, word_to_sentences_map: dict[str, str]
) -> Type[MarkdownTableWriter]:
    """
    Build a pytablewriter MarkdownTableWriter from data in a WordsWithFrequencyDict and a mapping
    between words and sample sentences,
    Format is 3 columns of word, documents containing the word and sample sentences with that word in from those documents

    Args:
        words_with_frequency: WordsWithFrequencyDict to build the table from
        word_to_sentences_map: mapping from words to sample sentences to build that c

    Returns: MarkdownTableWriter populated with the parameter data
    """
    if (
        not words_with_frequency
        or not all(v for v in words_with_frequency.values())
        or not word_to_sentences_map
    ):
        raise ValueError("Invalid Parameter")

    flattened_words = flatten_and_sort_words_with_frequency(words_with_frequency)

    value_matrix = []
    for word, frequency in flattened_words:
        # split('.')[0] is for removing the .txt from the filename
        docs = ", ".join(sorted(Path(path).stem for path in words_with_frequency[word]))
        value_matrix.append(
            [
                f"{word} ({frequency})",
                docs,
                "<br/><br/>".join(
                    highlight_text(sentence, word)
                    for sentence in word_to_sentences_map[word]
                ),
            ]
        )

    writer = MarkdownTableWriter(
        table_name="Interesting Words Summary",
        headers=[
            "Word (Total Occurances)",
            "Documents",
            "Sentences Containing The Word",
        ],
        value_matrix=value_matrix,
    )

    return writer


def build_filepaths_to_process(path: str) -> list[str]:
    """
    If path is a file then return that, if its a directory then add all the files inside

    Args:
        path: filepath, can be a file or directory

    Returns: List of filepaths
    """
    filepaths_to_process = []
    if os.path.isdir(path):
        directory_contents = os.listdir(path)
        filepaths_to_process = []
        for file in directory_contents:
            filename = os.path.join(path, file)
            if os.path.isfile(filename):
                filepaths_to_process.append(filename)
    else:
        filepaths_to_process.append(path)

    return filepaths_to_process


@click.command()
@click.argument("path", type=click.Path("r"))
@click.option(
    "--target", type=str, default="output.md", help="Filepath for the output table"
)
@click.option(
    "--unlimit-example-sentences",
    "example_limit",
    is_flag=True,
    help="Remove the one per document limit on example sentences in the table output",
)
@click.option(
    "--interesting-words-limit",
    "word_count",
    type=int,
    default=10,
    help="An upper bound on the number of interesting words in the output table, ranked by frequency, 0 means no limit",
)
@click.option(
    "--interesting-words-per-document",
    "per_doc_word_count",
    type=int,
    default=50,
    help="How many interesting words to discover per document, reducing improves performance but decreases validity",
)
def frequent_interesting_words(
    path, target, example_limit, word_count, per_doc_word_count
):
    """Extract the most frequent interesting words from a set of documents, then generate a table summarizing the results"""

    filepaths_to_process = build_filepaths_to_process(path)

    interesting_word_frequency_collection = []
    for filepath in filepaths_to_process:
        with open(filepath, "r") as f:
            text = f.read()
        interesting_word_frequency_collection.append(
            build_interesting_word_frequency_dict(
                text, filepath, word_limit=per_doc_word_count
            )
        )

    result = aggregate_words_with_frequency(
        interesting_word_frequency_collection, word_count
    )

    click.echo([k for k, _ in flatten_and_sort_words_with_frequency(result)])

    paths_to_word_map = defaultdict(list)
    for word, v in result.items():
        for path, _ in v.items():
            paths_to_word_map[path].append(word)

    # Second iteration to make sure one text file is kept in memory
    sentences = defaultdict(list)
    for filepath in filepaths_to_process:
        with open(filepath, "r") as f:
            text = f.read()
        for word in paths_to_word_map[filepath]:
            sentences[word] += extract_sample_sentences_from_text(
                word, text, None if example_limit else 1
            )

    format_output_table(result, sentences).dump(target)
