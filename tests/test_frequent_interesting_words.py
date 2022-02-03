import os

from click.testing import CliRunner

import frequent_interesting_words.cli as fiw_module
from frequent_interesting_words.cli import frequent_interesting_words

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURE_DIR = os.path.join(ROOT_DIR, "fixtures")


def test_frequent_interesting_words_bad_path():
    runner = CliRunner()
    result = runner.invoke(
        frequent_interesting_words, ["/cannot/exist/dear/heavens/no"]
    )
    assert result.exit_code == 2


def test_frequent_interesting_words_file():
    runner = CliRunner()
    with runner.isolated_filesystem() as td:
        result = runner.invoke(
            frequent_interesting_words, [f"{FIXTURE_DIR}/cats_and_mats.txt"]
        )
        assert result.exit_code == 0
        assert result.output == "['cat', 'mat', 'sat']\n"
        assert os.path.exists(f"{td}/output.md")

        with open(f"{td}/output.md") as f1, open(
            f"{FIXTURE_DIR}/cats_and_mats.md"
        ) as f2:
            assert f1.read() == f2.read()


def test_frequent_interesting_words_directory():
    runner = CliRunner()
    with runner.isolated_filesystem() as td:
        result = runner.invoke(
            frequent_interesting_words, [f"{FIXTURE_DIR}/path_directory"]
        )
        assert result.exit_code == 0
        assert result.output == "['cat', 'dog', 'bone', 'mat']\n"
        assert os.path.exists(f"{td}/output.md")

        with open(f"{td}/output.md") as f1, open(
            f"{FIXTURE_DIR}/path_directory.md"
        ) as f2:
            assert f1.read() == f2.read()


def test_frequent_interesting_words_target_output():
    runner = CliRunner()
    with runner.isolated_filesystem() as td:
        result = runner.invoke(
            frequent_interesting_words,
            [f"{FIXTURE_DIR}/cats_and_mats.txt", "--target", "target.md"],
        )
        assert result.exit_code == 0
        assert os.path.exists(f"{td}/target.md")


def test_frequent_interesting_words_unlimited_example_sentences(mocker):
    runner = CliRunner()
    with runner.isolated_filesystem() as td:
        result = runner.invoke(
            frequent_interesting_words,
            [f"{FIXTURE_DIR}/path_directory", "--unlimit-example-sentences"],
        )

        assert result.exit_code == 0
        assert os.path.exists(f"{td}/output.md")

        with open(f"{td}/output.md") as f1, open(
            f"{FIXTURE_DIR}/path_directory_unlimited_sentences.md"
        ) as f2:
            assert f1.read() == f2.read()


def test_frequent_interesting_words_interesting_words_limit(mocker):
    runner = CliRunner()
    with runner.isolated_filesystem() as td:
        result = runner.invoke(
            frequent_interesting_words,
            [f"{FIXTURE_DIR}/cats_and_mats.txt", "--interesting-words-limit", "1"],
        )
        assert result.exit_code == 0
        assert result.output == "['cat']\n"
        assert os.path.exists(f"{td}/output.md")


def test_frequent_interesting_words_interesting_words_per_document(mocker):
    runner = CliRunner()
    with runner.isolated_filesystem() as td:
        result = runner.invoke(
            frequent_interesting_words,
            [f"{FIXTURE_DIR}/path_directory", "--interesting-words-per-document", "1"],
        )
        assert result.exit_code == 0
        assert result.output == "['cat', 'dog']\n"
        assert os.path.exists(f"{td}/output.md")
