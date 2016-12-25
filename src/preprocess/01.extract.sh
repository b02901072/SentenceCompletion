#!/bin/bash

# Get rid of the irrelevant text in the raw corpus
raw_directory=$1
new_directory=$2
FILES=$raw_directory/*.TXT
for f in $FILES
do
  python extract.py $f $new_directory
done
