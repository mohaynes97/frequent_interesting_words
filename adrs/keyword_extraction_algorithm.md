# ADR 1 - Keyword Extraction Algorithm Selection

## Context

In order to determine the "interesting" words in a document we need to utilize a keyword extraction algorithm, of which there are many available in different libraries. Some measure of effectiveness must be applied to this choice.

## Options Assessed
* RAKE,  rake-nltk, v1.0.6
* YAKE, yake, v0.4.8
* BERT, keybert, v0.5.0

TF-IDF was also up for consideration but I could not find a sufficient political corpus easily so will be considered beyond the scope of this assessment

## Testing Criteria

The exercise requires the acquisition of the "interesting" words with the highest frequency. Frequency is assessed by the number of times the word appears in the document, "interesting" is assessed by eye measuring the top 10 keywords returned against the theme of each document provided for the exercise. As the measurement for "interesting" is far more vague in this context, frequency will be taken as a higher priority criteria.

The libraries themsleves are not explored in detail, each has recent changes, a release within the last year, support modern python versions and have a good number of stars and active community so they can all be taken as suitable.

Performance is also not thoroughly investigated as there are no SLA's associated with the exercise, however it can be taken as a secondary criteria.

The scripts for carrying out the tests are archived as ****, if any further clarification is needed

## Results

Results are formatted as [(a, b), ...) where a is the keyword and b is the frequency in the document 

### RAKE

| Document    | Result      |
| ----------- | ----------- |
| doc1.txt    | [('work', 12), ('years', 4), ('year', 3), ('words', 2), ('women', 2), ('write', 2), ('worst', 1), ('workers', 1), ('world', 1), ('worked', 1)]       |
| doc2.txt    | [('would', 8), ('workers', 6), ('working', 5), ('worked', 5), ('world', 3), ('wrote', 2), ('yes', 2), ('worn', 1), ('year', 1), ('yearn', 1)]       |
| doc3.txt    | [('world', 7), ('years', 6), ('would', 4), ('working', 2), ('work', 2), ('words', 2), ('yes', 2), ('write', 2), ('wrong', 1)]       |
| doc4.txt    | [('work', 9), ('yet', 4), ('women', 3), ('year', 2), ('willing', 1), ('win', 1), ('worse', 1), ('willingness', 1), ('wrongs', 1), ('wish', 1)]      |
| doc5.txt    | [('’', 24), ('would', 15), ('year', 11), ('world', 10), ('”', 8), ('without', 4), ('work', 3), ('working', 2), ('wounded', 1), ('written', 1)]       |
| doc6.txt    | [('weapons', 20), ('years', 6), ('way', 5), ('well', 3), ('world', 3), ('work', 3), ('weapon', 2), ('yet', 1), ('washington', 1), ('working', 1)]      |

In this case RAKE performs poorly for single keywords both in terms of relevancy and frequency, doc4.txt and doc5.txt being prime examples

### YAKE

| Document    | Result |
| ----------- | ----------- |
| doc1.txt    | [('people', 12), ('work', 12), ('today', 11), ('generation', 11), ('time', 10), ('america', 9), ('face', 8), ('war', 7), ('country', 6), ('long', 6)]       |
| doc2.txt    | [('promise', 31), ('america', 22), ('mccain', 20), ('time', 18), ('american', 18), ('country', 16), ('work', 16), ('john', 16), ('change', 15), ('americans', 8)]        |
| doc3.txt    | [('time', 13), ('america', 12), ('people', 12), ('care', 12), ('party', 12), ('country', 11), ('health', 9), ('government', 9), ('americans', 8), ('american', 5)]     |
| doc4.txt    | [('kenya', 27), ('people', 21), ('corruption', 19), ('country', 15), ('kenyan', 13), ('great', 11), ('nations', 10), ('african', 8), ('kenyans', 6), ('father', 5)]        |
| doc5.txt    | [('iraq', 54), ('iraqi', 24), ('war', 23), ('american', 21), ('troops', 20), ('government', 12), ('year', 11), ('iraqis', 9), ('forces', 9), ('americans', 6)]       |
| doc6.txt    | [('weapons', 20), ('threat', 16), ('soviet', 11), ('program', 10), ('reduction', 8), ('programs', 8), ('union', 8), ('russia', 6), ('cooperative', 6), ('russians', 5)]        |

YAKE produces keywords with a higher frequency then the other options as can be seen clearly in doc2.txt, in terms of quality it suffers from some redundancy and a bias towards proper nouns however the words are still relevant to the theme of the document and can be considered "interesting".

### BERT

| Document    | Result |
| ----------- | ----------- |
| doc1.txt    | [('state', 3), ('faith', 3), ('springfield', 3), ('peace', 2), ('illinois', 1), ('chicago', 1), ('churches', 1), ('christian', 1), ('secession', 1), ('righteousness', 1)]       |
| doc2.txt    | [('president', 9), ('clinton', 3), ('nomination', 1), ('presidency', 1), ('candidates', 1), ('biden', 1), ('obama', 1), ('nominee', 1), ('roosevelt', 1), ('candidate', 1)]        |
| doc3.txt    | [('agenda', 3), ('campaign', 2), ('politics', 2), ('election', 2), ('democrats', 2), ('progressive', 1), ('progress', 1), ('slogan', 1), ('crisis', 1), ('partisan', 1)]       |
| doc4.txt    | [('kenya', 27), ('kenyan', 13), ('african', 8), ('kenyans', 6), ('africa', 4), ('nairobi', 2), ('nkrumah', 1), ('kenyatta', 1), ('colonialism', 1), ('rwandan', 1)]        |
| doc5.txt    | [('war', 23), ('terrorism', 10), ('terrorists', 5), ('qaeda', 4), ('allies', 3), ('insurgents', 2), ('gettysburg', 1), ('terror', 1), ('nato', 1), ('freedoms', 1)]       |
| doc6.txt    | [('threat', 16), ('soviet', 11), ('security', 6), ('threats', 4), ('securing', 3), ('pathogen', 2), ('safety', 1), ('bioterrorism', 1), ('insurgencies', 1), ('safeguard', 1)]        |

BERT strongly succeeds in terms of generating interesting output with the words being topical and there being less redundancy and proper nouns compared to the other options, doc5.txt being exemplary however it fails on the frequency criteria producing far less frequent results which is especially noticable in the results for doc1.txt and doc2.txt.

This algorithm is also noticably less computationally performant then the others available

## Decision

Ultimately the high frequency count of YAKE along with its adequate quality of keywords combine to make it into the standout in spite of its lower quality output compared to BERT