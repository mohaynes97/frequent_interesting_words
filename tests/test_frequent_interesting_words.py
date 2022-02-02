import os

from click.testing import CliRunner

from cli import frequent_interesting_words

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


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
            frequent_interesting_words, [f"{ROOT_DIR}/fixtures/cats_and_mats.txt"]
        )
        assert result.exit_code == 0
        assert result.output == "['cat', 'mat', 'sat']\n"
        assert os.path.exists(f"{td}/output.md")


def test_frequent_interesting_words_directory():
    runner = CliRunner()
    with runner.isolated_filesystem() as td:
        result = runner.invoke(
            frequent_interesting_words, [f"{ROOT_DIR}/fixtures/path_directory"]
        )
        assert result.exit_code == 0
        assert result.output == "['cat', 'dog', 'bone', 'mat']\n"
        assert os.path.exists(f"{td}/output.md")


def test_frequent_interesting_words_target_output():
    runner = CliRunner()
    with runner.isolated_filesystem() as td:
        result = runner.invoke(
            frequent_interesting_words,
            [f"{ROOT_DIR}/fixtures/cats_and_mats.txt", "--target", "target.md"],
        )
        assert result.exit_code == 0
        assert os.path.exists(f"{td}/target.md")
