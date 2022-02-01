from collections import defaultdict
from pathlib import Path
from typing import List
from pytablewriter import MarkdownTableWriter

import yake
import nltk
import click
import os


def extract_keywords(text: str):
    """
    Get up to the top x keywords from text 
    
    """
    kw_extractor = yake.KeywordExtractor(lan="en", n=1, dedupLim=0.9, top=50, features=None)
    keywords = kw_extractor.extract_keywords(text)

    return [k[0].lower() for k in sorted(keywords, key=lambda x: x[1])]


def build_word_occurance_dict(text: str, words: List[str]) :
    """
    Build a dictionary of the frequency of words contained within a body of text
    """
    all_words = nltk.tokenize.TweetTokenizer(text).tokenize(text)
    stopwords = nltk.corpus.stopwords.words('english')
    lower_case_words = [k.lower() for k in words]
    filtered_words = nltk.FreqDist(w.lower() for w in all_words if w not in stopwords and w.lower() in lower_case_words)  

    return filtered_words


def build_interesting_word_frequency_dict(text: str, path: str):
    if not path or not text:
        return {}

    return {
        word: { path: frequency }
        for word, frequency in build_word_occurance_dict(text, extract_keywords(text)).items()
    }


def aggregate_words_with_frequency(interesting_word_frequency_collection):
    """merge the dicts"""
    result = defaultdict(dict)
    for interesting_word_frequency_dict in interesting_word_frequency_collection:
        for word, v in interesting_word_frequency_dict.items():
            for document, frequency in v.items():
                result[word][document] = frequency
    return result


def flatten_and_sort_words_with_frequency(words_with_frequency):
    flattened_words = [(k, sum(frequency for _, frequency in v.items() )) for k, v in words_with_frequency.items()]
    # ordered by frequency, followed by alphabetical
    return sorted(flattened_words, key=lambda x: (-x[1], x[0]))    


def extract_sample_sentences_from_text(keyword: str, text: str):
    """
    pulls a number of sample sentences from the text based on the keyword
    """
    if not keyword or not text: 
        return []

    sentences = nltk.tokenize.sent_tokenize(text)
    return [sentence for sentence in sentences if keyword.lower() in nltk.tokenize.word_tokenize(sentence.lower())]
 

def format_output_table(words_with_frequency, word_to_sentences_map):
    """
    Create the correct table writer    
    """
    if not words_with_frequency or not all(v for v in words_with_frequency.values()) or not word_to_sentences_map:
        raise ValueError("Invalid Parameter")

    flattened_words = flatten_and_sort_words_with_frequency(words_with_frequency)

    rows = []
    for word, frequency in flattened_words:
        rows.append([
            f"{word} ({frequency})", ", ".join(sorted(words_with_frequency[word])),
            "<br/><br/>".join(word_to_sentences_map[word])
        ])

    writer = MarkdownTableWriter(
        table_name="Interesting Words Summary",
        headers=["Word (Total Occurances)", "Documents", "Sentences Containing The Word"],
        value_matrix=rows
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
def frequent_interesting_words(path):
    filepaths_to_process = build_filepaths_to_process(path)
   
    interesting_word_frequency_collection = []
    for filepath in filepaths_to_process:        
        with open(filepath, "r") as f:
            text = f.read()
        interesting_word_frequency_collection.append(build_interesting_word_frequency_dict(text, filepath))

    result = aggregate_words_with_frequency(interesting_word_frequency_collection)
    processed_data = flatten_and_sort_words_with_frequency(result)

    click.echo([k for k, _ in processed_data])

    paths_to_word_map = defaultdict(list) 
    for word, v in result.items():
        for path, _ in v.items():
            paths_to_word_map[path].append(word)

    # second iteration to make sure one text file is kept in memory
    words = defaultdict(list)
    for filepath in filepaths_to_process:        
        with open(filepath, "r") as f:
            text = f.read()
        for word in paths_to_word_map[filepath]:
            words[word] += extract_sample_sentences_from_text(word, text)
    
    format_output_table(result, words).dump("welp.md")


if __name__ == '__main__':
    frequent_interesting_words()