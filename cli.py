from collections import defaultdict
from pathlib import Path
from tokenize import String
from typing import List
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
    Extract a list of the 10 most interesting words with frequency from a given document

    XXX: 10 limit not tested
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


def extract_sample_sentences_from_text(keyword: str, text: str):
    """
    pulls a number of sample sentences from the text based on the keyword
    
    returns as close to count as it can
    
    """
    if not keyword or not text: 
        return []

    sentences = nltk.tokenize.sent_tokenize(text)
    return [sentence for sentence in sentences if keyword.lower() in sentence.lower()]
 

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

    # flatten the format to a list of tuples
    flattened_words = [(k, sum(frequency for _, frequency in v.items() )) for k, v in result.items()]
    
    # turn to list ordered by size, followed by alphabetical
    flattened_words = [k for k, _ in sorted(flattened_words, key=lambda x: (-x[1], x[0]))]
    
    click.echo(flattened_words)

if __name__ == '__main__':
    frequent_interesting_words()