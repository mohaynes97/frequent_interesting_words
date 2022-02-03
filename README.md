# Frequent Interesting Words

A python CLI script for extracting the most frequent interesting words from a set of documents, then generating a table summarizing the results.

## Installation

**Requires Python3.9 and Pipenv installed** 

```bash
pipenv install
pipenv run setup_nltk
```

## Usage

```bash
# Arguments 
pipenv run frequent-interesting-words --help  
# Run on a single file
pipenv run frequent-interesting-words /sample_docs/doc1.txt
# Run on a directory
pipenv run frequent-interesting-words /sample_docs/
```
By default saves the table as **output.md** in the current directory

## Testing
```bash
pipenv install --dev
pipenv run pytest
```

## ADR's
Architectural decision records live in /adrs/

## License
[MIT](https://choosealicense.com/licenses/mit/)
