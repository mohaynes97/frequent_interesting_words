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


def extract_words_with_frequency_from_file(filepath: str):
    """
    Extract a list of the most interesting words with frequency from a given document
    """
    with open(filepath, "r") as f:
        text = f.read()

    keywords = extract_keywords(text)
    return build_word_occurance_dict(text, keywords)


def aggregate_words_with_frequency(filepaths: List[str]):
    filepaths = list(set(filepaths))
    result = defaultdict(dict)
    for file in filepaths:
        word_with_frequency_dict = extract_words_with_frequency_from_file(file)
        for word, frequency in word_with_frequency_dict.items():
            # remove the .txt from the file path
            result[word][Path(file).name[:-4]] = frequency
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
    return [sentence for sentence in sentences if keyword.lower() in sentence.lower()]
 

def format_output_table(words_with_frequency):
    """
    Create the correct table writer    
    """
    if not words_with_frequency or not all(v for v in words_with_frequency.values()):
        raise ValueError("Invalid Parameter")

    flattened_words = flatten_and_sort_words_with_frequency(words_with_frequency)

    rows = []
    for word, frequency in flattened_words:
        rows.append([f"{word} ({frequency})", ", ".join(sorted(words_with_frequency[word]))])

    writer = MarkdownTableWriter(
        table_name="Interesting Words Summary",
        headers=["Word (Total Occurances)", "Documents"],
        value_matrix=rows
    )

    return writer


@click.command()
@click.argument("path", type=click.Path("r"))
def frequent_interesting_words(path):
    if os.path.isdir(path): 
        directory_contents = os.listdir(path)
        files_to_process = []
        for file in directory_contents:
            filename = os.path.join(path, file)
            if os.path.isfile(filename):
                files_to_process.append(filename)
        result = aggregate_words_with_frequency(files_to_process)         
    else:
        result = aggregate_words_with_frequency([path])
    
    click.echo([k for k, _ in flatten_and_sort_words_with_frequency(result)])


if __name__ == '__main__':
    frequent_interesting_words()