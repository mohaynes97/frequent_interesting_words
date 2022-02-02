from collections import defaultdict
from pathlib import Path
from typing import List
from pytablewriter import MarkdownTableWriter
from yake.highlight import TextHighlighter

import yake
import nltk
import click
import os


def extract_keywords(text: str, word_limit: int):
    """
    Get up to the top x keywords from text 
    
    """
    kw_extractor = yake.KeywordExtractor(lan="en", n=1, dedupLim=0.9, top=word_limit, features=None)
    keywords = kw_extractor.extract_keywords(text)

    return [k[0].lower() for k in sorted(keywords, key=lambda x: x[1])]


def build_word_occurance_dict(text: str, words: List[str]) :
    """
    Build a dictionary of the frequency of words contained within a body of text
    """
    all_words = nltk.tokenize.word_tokenize(text)
    stopwords = nltk.corpus.stopwords.words('english')
    lower_case_words = [k.lower() for k in words]
    filtered_words = nltk.FreqDist(w.lower() for w in all_words if w not in stopwords and w.lower() in lower_case_words)  

    return filtered_words


def build_interesting_word_frequency_dict(text: str, path: str, word_limit: int):
    if not path or not text:
        return {}

    return {
        word: { path: frequency }
        for word, frequency in build_word_occurance_dict(text, extract_keywords(text, word_limit)).items()
    }


def flatten_and_sort_words_with_frequency(words_with_frequency):
    flattened_words = [(k, sum(frequency for _, frequency in v.items() )) for k, v in words_with_frequency.items()]
    # ordered by frequency, followed by alphabetical
    return sorted(flattened_words, key=lambda x: (-x[1], x[0]))    


def aggregate_words_with_frequency(interesting_word_frequency_collection, limit: int=None):
    """merge the dicts"""
    result = defaultdict(dict)
    for interesting_word_frequency_dict in interesting_word_frequency_collection:
        for word, v in interesting_word_frequency_dict.items():
            for document, frequency in v.items():
                result[word][document] = frequency
    
    if limit:
        result = { k: v for k, v in result.items() if k in [x for x, _ in flatten_and_sort_words_with_frequency(result)[:limit]] }
    return result


def extract_sample_sentences_from_text(keyword: str, text: str, limit: int=None):
    """
    pulls a number of sample sentences from the text based on the keyword
    """
    if not keyword or not text: 
        return []

    sentences = nltk.tokenize.sent_tokenize(text)
    sample_sentences = [sentence for sentence in sentences if keyword.lower() in nltk.tokenize.word_tokenize(sentence.lower())]
    if limit:
        sample_sentences = sample_sentences[:limit]
    return sample_sentences


def highlight_text(text: str, word: str):
    return TextHighlighter(max_ngram_size=1, highlight_pre="**", highlight_post="**").highlight(text, [word, f"{word}'s"])    


def format_output_table(words_with_frequency, word_to_sentences_map):
    """
    Create the correct table writer    
    """
    if not words_with_frequency or not all(v for v in words_with_frequency.values()) or not word_to_sentences_map:
        raise ValueError("Invalid Parameter")

    flattened_words = flatten_and_sort_words_with_frequency(words_with_frequency)

    value_matrix = []
    for word, frequency in flattened_words:
        # [:-4] is for removing the .txt from the filename
        docs = ", ".join(sorted(Path(path).name[:-4] for path in words_with_frequency[word]))
        value_matrix.append([
            f"{word} ({frequency})", docs, "<br/><br/>".join(
                highlight_text(sentence, word) for sentence in word_to_sentences_map[word]
            )
        ])

    writer = MarkdownTableWriter(
        table_name="Interesting Words Summary",
        headers=["Word (Total Occurances)", "Documents", "Sentences Containing The Word"],
        value_matrix=value_matrix
    )

    return writer


def build_filepaths_to_process(path: str):
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
@click.option('--target', type=str, default="output.md", help="Filepath for the output table")
@click.option('--unlimit-example-sentences', 'example_limit', is_flag=True, help="Remove the one per document limit on example sentences in the table output")
@click.option('--interesting-words-limit', 'word_count', type=int, default=10, help="An upper bound on the number of interesting words in the output table, ranked by frequency, 0 means no limit")
@click.option('--interesting-words-per-document', 'per_doc_word_count', type=int, default=50, help="How many interesting words to discover per document, reducing improves performance but decreases validity")
def frequent_interesting_words(path, target, example_limit, word_count, per_doc_word_count):
    filepaths_to_process = build_filepaths_to_process(path)
   
    interesting_word_frequency_collection = []
    for filepath in filepaths_to_process:        
        with open(filepath, "r") as f:
            text = f.read()
        interesting_word_frequency_collection.append(build_interesting_word_frequency_dict(text, filepath, word_limit=per_doc_word_count))

    result = aggregate_words_with_frequency(interesting_word_frequency_collection, word_count)
    processed_data = flatten_and_sort_words_with_frequency(result)
   
    click.echo([k for k, _ in processed_data])

    paths_to_word_map = defaultdict(list) 
    for word, v in result.items():
        for path, _ in v.items():
            paths_to_word_map[path].append(word)

    # second iteration to make sure one text file is kept in memory
    sentences = defaultdict(list)
    for filepath in filepaths_to_process:        
        with open(filepath, "r") as f:
            text = f.read()
        for word in paths_to_word_map[filepath]:
            sentences[word] += extract_sample_sentences_from_text(word, text, None if example_limit else 1)
    
    format_output_table(result, sentences).dump(target)


if __name__ == '__main__':
    frequent_interesting_words()