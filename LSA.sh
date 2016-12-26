MSR_TEST=data/MSR_Sentence_Completion_Challenge_V1
QUESTION=$MSR_TEST/Data/Holmes.machine_format.questions.txt
ANSWER=$MSR_TEST/Data/Holmes.machine_format.answers.txt

MODEL=model
WORD2VEC_MODEL=$MODEL/key.150.model

STOP_WORDS=data/stop_words.txt

RESULT=$1

NEIGHBOR=data/neighbor
FEATURE_1=$NEIGHBOR/neighbor.bi.1.csv
FEATURE_2=$NEIGHBOR/neighbor.bi.2.csv

if [ -f $RESULT ]; then
  rm $RESULT
fi
python src/LSA.py $WORD2VEC_MODEL $QUESTION $RESULT $FEATURE_1 $FEATURE_2 $STOP_WORDS
$MSR_TEST/score.pl $RESULT $ANSWER #&> /dev/null
