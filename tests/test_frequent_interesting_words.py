from click.testing import CliRunner
from cli import frequent_interesting_words
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def test_frequent_interesting_words_bad_path():
    runner = CliRunner()
    result = runner.invoke(frequent_interesting_words, ["/cannot/exist/dear/heavens/no"])
    assert result.exit_code == 2


def test_frequent_interesting_words_file():
  runner = CliRunner()
  result = runner.invoke(frequent_interesting_words, [f"{ROOT_DIR}/fixtures/cats_and_mats.txt"])
  assert result.exit_code == 0

  
def test_frequent_interesting_words_directory():
  runner = CliRunner()
  result = runner.invoke(frequent_interesting_words, [f"{ROOT_DIR}/fixtures/path_directory"])
  assert result.exit_code == 0