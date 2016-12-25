#!/usr/bin/python

import sys
import os
import re

# How to use
# $ python extract.py <INPUT_TXT> <OUTPUT_DIRECTORY>
if len(sys.argv) != 3:
    exit()
target_path = sys.argv[1]
(target_directory, target_base) = os.path.split(target_path) 
output = sys.argv[2] + target_base
with open(target_path, "r") as f:
    data = f.read()
    f.closed
print "Processing: ", target_base

start1 = data.find("*END*")
start2 = data.find("*END*", start1+5)
end1 = data.find("End of the Project Gutenberg")
end2 = data.find("End of Project Gutenberg")
end3 = data.find("End of The Project Gutenberg")
end = max(end1, end2, end3)
data = data[(start2+5):end]

print "Saving ", output 
with open(output, "w") as f:
    f.write(data)
    f.closed

