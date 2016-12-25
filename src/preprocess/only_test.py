#!/usr/bin/python

import sys
import os
import numpy as np

# USAGE: 
# $ python THIS.PY <INPUT_TXT> <TEST_WORD_TXT> <OUTPUT_TXT>

''' Input '''
input_file = sys.argv[1]
with open(input_file, "r") as f:
    input_data = f.read()
    f.close()

test_word_file = sys.argv[2]
test_words = list(np.genfromtxt(test_word_file, delimiter=' ', dtype='str')[:, 0])
test_words = [w.lower() for w in test_words]

''' Output '''
output_file = sys.argv[3]
lines = input_data.split('\n')
with open(output_file, 'w') as f:
    for line in lines:
        line = line.strip()
        words = line.split()
        isTest = False
        for word in words:
            if len(word) == 0:
                continue
            if word[0] == "<":
                continue
            if word.lower() in test_words:
                isTest = True
                break
        if isTest:
            f.write(line + '\n')
    f.close()



