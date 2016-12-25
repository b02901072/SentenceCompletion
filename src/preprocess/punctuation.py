#!/usr/bin/python

import sys
import os
import re

# Usage:e
# $ python THIS.PY <INPUT_TXT> <OUTPUT_TXT>

''' Input '''
input_txt = sys.argv[1]
with open(input_txt, "r") as f:
    data = f.read()
    f.closed

''' Output '''
output_txt = sys.argv[2]

# Removing ^M ('\r')
data = data.replace("\r", "")
data = data.replace("\n\n", ".")
data = data.replace("\n", " ")

data = data.replace("--", ", ")
data = data.replace(" - ", " ")
data = data.replace("_", "")
data = data.replace("[", "")
data = data.replace("]", "")
data = data.replace("-", "_")
data = re.sub("[()\"]", "\n", data)

data = re.sub("[/{/}^,`*$]", "", data)
data = re.sub("[.:;?!]", "\n", data)

lines = data.split('\n')
with open(output_txt, "w") as f:
    for line in lines:
        line = line.strip()
        if line != "":
            f.write(line + '\n')
    f.closed

