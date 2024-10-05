# Use Python, Scala or Java to produce a CSV file with top five word 3-grams (n-grams, use lowercase and remove
# punctuation) in the commit messages for each author name in event type “PushEvent” within the file 10K.github.jsonl.bz2.
# Output example:
# 'author' 'first 3-gram' 'second 3-gram' 'third 3-gram' 'fourth 3-gram' 'fifth 3-gram'
# 'erfankashani' 'merge pull request' 'pull request #4' 'request #4 from' 'rack from 207' 'from 207 to'


import os
import string
import json
import csv
from collections import Counter

import nltk
from nltk import ngrams

nltk.download("punkt_tab")

data = (
    json.loads(line)
    for line in open("M01_Introduction_Python/10K.github.jsonl (1) (1)", "r")
)

commits = []
for record in data:
    if record["type"] == "PushEvent":
        commits.extend(record["payload"]["commits"])

commits_by_author: dict[str, list] = {}
for commit in commits:
    commits_by_author.setdefault(commit["author"]["name"], []).append(commit["message"])

trigrams_by_author: dict[str, list] = {}
for author, commit_messages in commits_by_author.items():
    for msg in commit_messages:
        tokens = nltk.word_tokenize(msg)
        tokens = [token.lower() for token in tokens if token not in string.punctuation]
        trigrams = ngrams(tokens, 3)
        trigrams_by_author.setdefault(author, []).extend(trigrams)

parent_dir = "M01_Introduction_Python"
trigrams_file = os.path.join(parent_dir, "trigrams.csv")

with open(trigrams_file, "w", newline="") as file:
    writer = csv.writer(file)

    for author, trigrams in trigrams_by_author.items():
        trigram_freq = Counter(trigrams)
        top_five_trigrams = [
            ", ".join(trigram) for trigram, _ in trigram_freq.most_common(5)
        ]
        top_five_trigrams += [""] * (5 - len(top_five_trigrams))
        writer.writerow([author] + top_five_trigrams)
