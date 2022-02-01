import pytest
from cli import format_output_table
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def test_generate_table_empty_parameters():
    with pytest.raises(ValueError):
        format_output_table({}, {})


def test_generate_table_inner_empty_parameters():
    with pytest.raises(ValueError):
        format_output_table({'word': {}, 'word2': {'file': 1} }, {})


def test_generate_table_empty_word_to_sentence_map():
    with pytest.raises(ValueError):
        format_output_table({'word': {'file': 1}, 'word2': {'file': 1} }, {})


def test_generate_table_one_doc():
    writer = format_output_table({'word': {'/welp/doc.txt': 1} }, { 'word': ['A terrible word.', 'The power of a word.']})
    with open(f"{ROOT_DIR}/fixtures/test_generate_table_one_doc.md") as f:
        assert writer.dumps() == f.read()


def test_generate_table_multiple_docs():
    writer = format_output_table(
        {'word': {'/welp/doc2.txt': 3, '/welp/doc1.txt': 1}, 'word2': {'/welp/doc1.txt': 1 } },
        {
            'word': ['A terrible word.', 'The power of a word.'],
            'word2': ['Oh word2, so silly!']
        }
    )
    
    with open(f"{ROOT_DIR}/fixtures/test_generate_table_multiple_docs.md") as f:
        assert writer.dumps() == f.read()