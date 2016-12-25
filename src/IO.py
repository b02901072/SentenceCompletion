import numpy as np
import re

def readVec(file):
    # read train_vectors.txt
    # return dictionary of word vectors
    with open(file, "r+") as f:
        vecDict = {}
        for line in f:
            vec = re.split(" |\n", line[:-1])   # delete '\n'
            if vec[-1] == "":
                vecDict[vec[0]] = np.array(vec[1:-1], dtype = np.float)
                # vecDict[vec[0]] = vec[1:-1]
            # print vecDict
    return vecDict

def readVocab(file):
    # read train_vocab.txt
    # return dictionary of vocab numbers
    with open(file, "r+") as f:
        vocabDict = {}
        cnt = 0
        for line in f:
            vocab = re.split(" |\n", line[:-1])   # delete '\n'
            if vocab[-1] == "":   # first line end with '\n' while others with ' '
                vocabDict[vocab[0]] = cnt
                cnt += 1
    return vocabDict

def readSentVec(file, Dict, v):
    # return list of training datas ( word vectors )
    with open(file, "r+") as f:
        vecSentList = []
        for line in f:
            vecSent = []
            line = line.replace("\n", " ")
            sent = re.split(" ", line)
            if v:
                print sent
            for i in sent:
                if i != "":
                    i = i.replace("\'", "")
                    if i in Dict:
                        vecSent.append(Dict[i])
                    else:
                        vecSent.append(Dict["<oov>"])
                        print i, "not in dict"
            vecSentList.append(vecSent)
    return vecSentList

def readSentVocabVec(file, Dict):
    # return list of 1-N labels
    vocab_size = len(Dict)
    with open(file, "r+") as f:
        vocabSentList = []
        for line in f:
            vocabSent = []
            line = line.replace("\n", " ")
            sent = re.split(" ", line)
            for i in sent:
                if i != "":
                    i = i.replace("\'", "")
                    if i in Dict:
                        c = np.zeros(vocab_size)
                        c[Dict[i]] = 1
                        vocabSent.append(c)
                    else:
                        print i, "not in dict"
            vocabSentList.append(vocabSent)
    return vocabSentList

def readSentVocabNum(file, Dict):   
    # return vocab numbers of words
    # for scoring testing data
    vocab_size = len(Dict)
    with open(file, "r+") as f:
        vocabSentList = []
        for line in f:
            vocabSent = []
            line = line.replace("\n", " ")
            sent = re.split(" ", line)
            for i in sent:
                if i != "":
                    i = i.replace("\'", "")
                    if i in Dict:
                        vocabSent.append(Dict[i])
                    else:
                        print i, "not in dict"
            vocabSentList.append(vocabSent)
    return vocabSentList

def test1_N(file, vecDict, vocabDict):
    x = readSentVec(file, vecDict)  # word vectors
    y = readSentVocabNum(file, vocabDict)  # numbers of vocab id
    scoreList = []
    cnt = 0
    for i in range(len(x)):
        # yy_pred is a list of prob vectors
        yy_pred = model.predict(np.array(x[i][:-1]), batch_size = 64)
        score = 0
        for j in range(len(y[i])-1):
            score += yy_pred[y[i][j+1]]
        scoreList.append(score)
        cnt += 1
        if cnt % 5 == 0:
            maxchoice = 0
            scoremax = scoreList[0]
            for j in range(5):
                if scoreList[j] > scoremax:
                    maxchoice = j
                    scoremax = scoreList[j]
            print maxchoice
            scoreList = []
    return


