#!/usr/bin/python

import os
import sys

# Check if a string is a NUMBER or not
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Parsing
# How to use
# $ python dictionary.py <INPUT_TXT> 
target_path = sys.argv[1]
(target_directory, target_base) = os.path.split(target_path) 
output = target_base + ".word"
wordcount = target_base + ".count"
with open(target_path, "r") as f:
    data = f.read()
    f.closed

lines = data.split('\n')
line_num = len(lines)
data = ""
not_name_list = []
word_dict = dict()
word_dict["<num>"] = 0
word_dict["<month>"] = 0
word_dict["<name>"] = 0
word_dict["<oov>"] = 0
for line in lines:
    line = line.strip()
    words = line.split(" ")
    isFirst = True
    line = ""
    for word in words:
        if len(word) == 0:
            continue
        if is_number(word):
            word = "<num>"
        if isFirst:
            isFirst = False
            word = word.lower()    
        if word[0] >= 'A' and word[0] <= 'Z':
            if is_month(word):
                word = "<month>"
            if word == "I":
                word = "i"
        if word[0] == '<' or (word[0] >= 'a' and word[0] <= 'z'):
            word = word.lower()
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
        line += word + " "
    data += line + "\n"

lines = data.split('\n')
data = ""
for line in lines:
    line = line.strip()
    words = line.split(" ")
    line = ""
    for word in words:
        if len(word) == 0:
            continue
        if word[0] >= 'A' and word[0] <= 'Z':
            word = word.lower()
            if word in word_dict:
                word_dict[word] += 1
            else:
                print word
                word = "<name>"
                word_dict["<name>"] += 1
        line += word + " "
    if len(line) != 0:
        data += line + '\n'

lines = data.split('\n')
data = ""
for line in lines:
    line = line.strip()
    words = line.split(" ")
    line = ""
    for word in words:
        if len(word) == 0:
            continue
        if word in word_dict:
            if word_dict[word] <= 10:
                word = "<oov>"
                word_dict["<oov>"] += 1
        else:
            word = "<oov>"
            word_dict["<oov>"] += 1
        line += word + " "
    data += line + '\n'


with open(output, "w") as f:
    f.write(data)
    f.closed

dict_data = ""
new_word_dict = dict()
new_word_dict["<oov>"] = 0
for word in iter(word_dict):
    if word_dict[word] <= 10:
        new_word_dict["<oov>"] += word_dict[word]
    else:
        new_word_dict[word] = word_dict[word]
for word in iter(new_word_dict):
    dict_data += (word + " " + str(new_word_dict[word]) + "\n")
with open(wordcount, "w") as f:
    f.write(dict_data)
    f.closed

