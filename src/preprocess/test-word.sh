SIZE=200
ITER=15
time ./word2vec/word2vec -train ./data/testing/Data/Holmes.lm_format.questions.txt -output ./data/test_vectors.txt -cbow 1 -size $SIZE -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 5 -binary 0 -iter $ITER -min-count 1 -save-vocab ./data/test_vocab.txt

