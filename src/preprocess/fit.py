#!/usr/bin/python

import sys
import os

# Parsing
# How to use
# $ python preprocess.py <INPUT_TXT> <TEST_WORD_TXT>
target_path = sys.argv[1]
output = sys.argv[3]
with open(target_path, "r") as f:
    data = f.read()
    f.closed

test_word_path = sys.argv[2]
with open(test_word_path, "r") as f:
    test_word_data = f.read()
    f.closed
lines = test_word_data.split('\n')
test_words = []
for line in lines:
    line = line.strip()
    if len(line) == 0:
        continue
    words = line.split()
    test_words.append(words[0].lower())

lines = data.split('\n')
data = ""
name_list = []
for line in lines:
    line = line.strip()
    words = line.split(" ")
    isTest = True
    line = ""
    for word in words:
        if len(word) == 0:
            continue
        if word[0] == "<":
            continue
        if isTest == True:
            if word not in test_words:
                isTest = False
        line += " " + word
    line = line.strip()
    if isTest == True:
        data += line + '\n'

with open(output, "w") as f:
    f.write(data)
    f.closed


