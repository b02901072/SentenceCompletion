#!/bin/bash
text_directory=$1
FILES=$text_directory/*.TXT

if [[ ! -e $text_directory/input ]]
then
  mkdir $text_directory/input
else
  rm -rf $text_directory/input/*
fi

if [[ ! -e $text_directory/output ]]
then
  mkdir $text_directory/output
else
  rm -rf $text_directory/output/*
fi

for f in $FILES
do
  python preprocess.py $f
done
