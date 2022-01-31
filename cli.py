# 1. fetch x top keywords from each document, with frequency
# 2. aggregate and format int
# 3. export in the output format

from collections import defaultdict
from typing import List
import yake
import nltk
import click
import os


def extract_keywords(text: str):
    """
    Get up to the top 10 keywords from text 
    
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
    Extract a list of the 10 most interesting words with frequency from a given document

    XXX: 10 limit not tested
    """
    with open(filepath, "r") as f:
        text = f.read()

    keywords = extract_keywords(text)
    return build_word_occurance_dict(text, keywords)


def aggregate_words_with_frequency(filepaths: List[str]):
    result = defaultdict(int)
    for file in filepaths:
        word_with_frequency_dict = extract_words_with_frequency_from_file(file)
        for word, frequency in word_with_frequency_dict.items():
            result[word] += frequency
    return result


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
        aggregate_words_with_frequency(files_to_process)         
    else:
        aggregate_words_with_frequency([path])


if __name__ == '__main__':
    frequent_interesting_words()