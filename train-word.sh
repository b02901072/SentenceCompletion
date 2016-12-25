SIZE=125
ITER=15
train=$1
output=$2

time ./word2vec/word2vec -train $1 -output $2 -cbow 1 -size $SIZE -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 5 -binary 0 -iter $ITER -min-count 1 

