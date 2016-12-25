./train-word.sh
python src/LSA_main.py
./data/testing/score.pl result/test.ans.txt data/testing/Data/Holmes.machine_format.answers.txt
