#!/usr/bin/python

import os
import sys
import re

# Check if a string is a MONTH or not
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
def is_month(s):
    for m in MONTHS:
        if s == m:
            return True
    return False

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

data = re.sub("[/'/{/}^,`*$;:]", "", data)
data = data.replace("<s>", "")

count_list_path = sys.argv[2]
with open(count_list_path, "r") as f:
    count_list_data = f.read()
    f.closed
lines = count_list_data.split('\n')
not_name_list = []
for line in lines:
    line = line.strip()
    words = line.split(" ")
    line = ""
    for word in words:
        if len(word) == 0:
            continue
        not_name_list.append(word)
        break
not_name_list.append("<s>")
not_name_list.append("</s>")

lines = data.split('\n')
line_num = len(lines)
data = ""
max_sent_length = 0
for line in lines:
    line = line.strip()
    words = line.split(" ")
    isFirst = True
    line = ""
    if len(words) > max_sent_length:
        max_sent_length = len(words)
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
        word = word.lower()
        if word[0] == '<' or (word[0] >= 'a' and word[0] <= 'z'):
            if word not in not_name_list:
                word = "<name>"
        line += word + " "
    data += line + "\n"

lines = data.split('\n')
data = ""
for line in lines:
    line = line.strip()
    words = line.split(" ")
    line = ""
    count = 0
    if len(words) == 0:
        continue
    for word in words:
        count += 1
        if count == 1:
            line += word
        else:
            line += " " + word
    i = count
    while i < max_sent_length:
        line += " </s>"
        i += 1
    data += line + '\n'


with open(output, "w") as f:
    f.write(data)
    f.closed

