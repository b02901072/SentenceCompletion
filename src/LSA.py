import re
import numpy as np
import IO
import sys
from sklearn.metrics.pairwise import cosine_similarity
import random

word2vec_model_file = sys.argv[1]
vecDict = IO.readVec(word2vec_model_file)
questions_file = sys.argv[2]
result_file = sys.argv[3]
feature_1_file = sys.argv[4]
feature_2_file = sys.argv[5]

stop_words_file = sys.argv[6]
stop_words = ['\"', '', 'ROOT', '.', ',']
with open(stop_words_file, 'r') as f:
    for line in f:
        stop_words.append(line[:-1])

features_1_list = []
with open(feature_1_file, 'r') as f:
    for line in f:
        line = re.sub('[\r\n]', '', line)
        words = line.split(',')
        features = set()
        for word in words:
            if word not in stop_words:
                features.update([word.lower()])
        features_1_list.append(features)
    f.close()

features_2_list = []
with open(feature_2_file, 'r') as f:
    for line in f:
        line = re.sub('[\r\n]', '', line)
        words = line.split(',')
        features = set()
        for word in words:
            if word not in stop_words:
                features.update([word.lower()])
        features_2_list.append(features)
    f.close()

CHOICE_NUM = 5
WINDOW_SIZE = 5

result_content = ''
with open(result_file, 'w') as fw:
    with open(questions_file, "r+") as f:
        choices = []
        count = 0
        for line in f:
            choices.append(line[:-1])
            if len(choices) < CHOICE_NUM:
                continue
            
            count += 1
            features_1 = list(features_1_list[count-1])
            features_2 = list(features_2_list[count-1])

            similarity = np.zeros(CHOICE_NUM)
            for choice in range(CHOICE_NUM):
                score = 0
                sentence = choices[choice].lower()
                start = sentence.find(")")
                sentence = sentence[start+2:]
                words = sentence.split(' ')

                key_index = 0
                key = ""
                for i in range(len(words)):
                    word = words[i]
                    if word[0] == '[':
                        key_index = i
                        key = word[1:-1]
                        words[i] = key
                        break
                word_count = 0
                if key not in vecDict:
                    score = 0.0
                else:
                    vec_1 = np.reshape(vecDict[key], (1, -1))
                    for i in range(len(words)):
                        if i != key_index:
                            word = words[i]
                            weight = 0.0
                            if abs(i - key_index) > WINDOW_SIZE:
                                weight = 0.0
                            if word in features_2:
                                weight = 2.0
                            if word in features_1:
                                weight = 4.0
                            if word in vecDict and word not in stop_words:
                                vec_2 = np.reshape(vecDict[word], (1, -1))
                                sim = cosine_similarity(vec_1, vec_2)
                                word_count += 1
                                score += weight*sim
                if word_count == 0:
                    word_count = 1
                similarity[choice] = score / word_count
            
            answer = np.argmax(similarity)
            fw.write(choices[answer] + '\n')

            if len(choices):
                del choices[:]
        f.close()  
    fw.close()
