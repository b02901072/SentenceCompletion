MSR_TEST=data/MSR_Sentence_Completion_Challenge_V1/
QUESTION=$MSR_TEST/Holmes.machine_format.questions.txt

MODEL=model/
WORD2VEC_MODEL=$model/key.125.model

STOP_WORDS=data/stop_words.txt

RESULT=$1

FEATURE_1=data/neighbor.bi.1.csv
FEATURE_2=data/neighbor.bi.2.csv

ANSWER=data/testing/Data/Holmes.machine_format.answers.txt

if [ -f $RESULT ]; then
  rm $RESULT
fi
python src/LSA.py $WORD2VEC_MODEL $QUESTION $RESULT $FEATURE_1 $FEATURE_2 $STOP_WORDS
./data/testing/score.pl $RESULT $ANSWER #&> /dev/null
