#!/usr/bin/python

import sys
import os
import re

# Parsing
# How to use
# $ python preprocess.py <INPUT_TXT> <TEST_WORD_TXT>
target_path = sys.argv[1]
(target_directory, target_base) = os.path.split(target_path) 
neat = target_base + ".neat"
input_text = target_base + ".input"
output_text = target_base + ".output"
with open(target_path, "r") as f:
    data = f.read()
    f.closed

with open("data.TXT.punc.count", "r") as f:
    word_dict_data = f.read()
    f.closed
lines = word_dict_data.split('\n')
word_list = []
for line in lines:
    line = line.strip()
    words = line.split(" ")
    word_list.append(words[0])

lines = data.split('\n')
input_data = ""
output_data = ""
max_length = 40
for line in lines:
    line = line.strip()
    words = line.split(" ")
    input_line = ""
    output_line = ""
    count = 0
    if len(words) == 0:
        continue
    for word in words:
        count += 1
        if count == 1:
            input_line += word
        elif count == 2:
            output_line += word
        if count >= 2 and count <= max_length:
            input_line += " " + word
        if count >= 3 and count <= max_length+1:
            output_line += " " + word
        if count > max_length:
            break
    i = count
    while i < max_length:
        input_line += " </s>"
        i += 1
    j = count
    while j < max_length+1:
        output_line += " </s>"
        j += 1
    output_data += output_line + '\n'
    input_data += input_line + '\n'

print "Saving ", input_text
with open(input_text, "w") as f:
    f.write(input_data)
    f.closed

print "Saving ", output_text
with open(output_text, "w") as f:
    f.write(output_data)
    f.closed

