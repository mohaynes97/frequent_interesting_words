import pytest
from cli import format_output_table
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def test_generate_table_empty_parameters():
    with pytest.raises(ValueError):
        format_output_table({})


def test_generate_table_inner_empty_parameters():
    with pytest.raises(ValueError):
        format_output_table({'word': {}, 'word2': {'file': 1} })


def test_generate_table_one_doc():
    writer = format_output_table({'word': {'doc': 1} })
    with open(f"{ROOT_DIR}/fixtures/test_generate_table_one_doc.md") as f:
        assert writer.dumps() == str(f.read())


def test_generate_table_multiple_docs():
    writer = format_output_table({'word': {'doc2': 3, 'doc1': 1}, 'word2': {'doc1': 1 } })
    with open(f"{ROOT_DIR}/fixtures/test_generate_table_multiple_docs.md") as f:
        assert writer.dumps() == f.read()