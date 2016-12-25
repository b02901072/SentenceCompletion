#!/bin/bash
DIR=$1
FILES=$DIR/*.TXT
cat $FILES > $DIR/Holmes_all.TXT
