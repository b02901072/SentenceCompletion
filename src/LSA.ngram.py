import re
import numpy as np
import IO

ngram = 4

def test(file, dict):
    ansFile = open("result/test.ans.4.txt", 'w')
    with open(file, "r+") as f:
        sim = []
        count = 0
        for line in f:
            print line
            sent = line[:-1].replace("--", ", ")
            sent = sent.replace(" - ", " ")
            sent = sent.replace("-", "_")
            sent = sent.replace("\"", "")
            sent = sent.replace("\'", "")
            sent = sent.replace(",", "")
            sent = re.split("\) | \[|\] ", sent)
            if sent[2] != "I":
                key = sent[2].lower()
            else:
                key = sent[2]
            sent = re.split("\W+", sent[1]) + [sent[2]] + re.split("\W+", sent[3])
            sent = sent[:-1]
            score = 0
            if key in dict:
                for i in range( len( sent ) ):
                    if sent[i] == key:
                        if i < ngram:
                            for j in range(2 * ngram + 1):
                                if j < len ( sent ):
                                    if sent[j] != "I":
                                        sent[j] = sent[j].lower()
                                    if sent[j] != "":
                                        if sent[j] in dict:
                                            score += np.dot(dict[key], dict[sent[j]]) / np.sqrt(np.dot(dict[key], dict[key]) * np.dot(dict[sent[j]], dict[sent[j]]))
                        elif i > len( sent ) - ngram - 1:
                            for j in range(2 * ngram + 1):
                                k = len( sent ) - j;
                                if k >= 0 and k < len( sent ):
                                    if sent[k] != "I":
                                        sent[k] = sent[k].lower()
                                    if sent[k] != "":
                                        if sent[k] in dict:
                                            score += np.dot(dict[key], dict[sent[k]]) / np.sqrt(np.dot(dict[key], dict[key]) * np.dot(dict[sent[k]], dict[sent[k]]))
                        else :
                            for j in range(2 * ngram + 1):
                                k = i - ngram + j
                                if sent[k] != "I":
                                    sent[k] = sent[k].lower()
                                if sent[k] != "":
                                    if sent[k] in dict:
                                        score += np.dot(dict[key], dict[sent[k]]) / np.sqrt(np.dot(dict[key], dict[key]) * np.dot(dict[sent[k]], dict[sent[k]]))

                # for i in sent:
                    # if i != "I":
                        # i = i.lower()
                    # if i != "":
                        # if i in dict:
                            # score += np.dot(dict[key], dict[i]) / np.sqrt(np.dot(dict[key], dict[key]) * np.dot(dict[i], dict[i]))
            sim += [(line, score)]
            
            count += 1
            if count % 5 == 0:
                maxAns = sim[0][0]
                max = sim[0][1]
                for i in sim:
                    if max < i[1]:
                        maxAns = i[0]
                        max = i[1]
                ansFile.write(maxAns)
                sim = []
    return

Dict = IO.readVec("data/train_vectors.1.txt")
test("data/testing/Data/Holmes.machine_format.questions.txt", Dict)
