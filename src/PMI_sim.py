import re
import numpy as np
import IO
import sys
import random
try:
	import cpickle as pickle
except:
	import pickle

dpmi_model_file = sys.argv[1]
dpmi = np.load(dpmi_model_file)
vocab_file = sys.argv[2]
vocabs = pickle.load(open(vocab_file, 'r'))
v_str_to_id = {}
for i in vocabs:
	v = vocabs[i]
	v_str_to_id[v] = i

questions_file = sys.argv[3]
result_file = sys.argv[4]

feature_1_file = sys.argv[5]
feature_2_file = sys.argv[6]

stop_words_file = sys.argv[7]
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
				weight_sum = 0.0
				if key not in v_str_to_id:
					score = 0.0
				else:
					key_id = v_str_to_id[key]
					for i in range(len(words)):
						weight = 0.0
						if i != key_index:
							word = words[i]
							if word in stop_words:
								continue
							if word not in v_str_to_id:
								continue
							if word in features_2:
								weight = 0.0
							if word in features_1:
								weight = 4.0
							weight_sum += weight
							word_id = v_str_to_id[word]
							score += weight * dpmi[key_id][word_id]

				similarity[choice] = score / max(weight_sum, 1.0)
			
			answer = np.argmax(similarity)
			fw.write(choices[answer] + '\n')

			if len(choices):
				del choices[:]
		f.close()  
	fw.close()
