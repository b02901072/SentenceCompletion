SIZE=200
ITER=15
time ./word2vec/word2vec -train data.TXT.punc.word -output ./data/train_vectors.10.txt -cbow 1 -size $SIZE -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 5 -binary 0 -iter $ITER -min-count 10 -save-vocab ./data/train_vocab.10.txt

