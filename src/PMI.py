import sys
import numpy as np
import math

holmes_corpus_file = sys.argv[1]
pmi_model_file = sys.argv[2]
stop_words_file = sys.argv[3]
stop_words = []
with open(stop_words_file, 'r') as f:
    for line in f:
        stop_words.append(line[:-1])

cooccurence = {}
line_count = 1
word_count = 0
print('Counting cooccurence...')
with open(holmes_corpus_file, 'r') as f:
	for line in f:
		print(line_count)
		line_count += 1
		if line_count > 10000:
			break
		words = line[:-1].split()
		word_count += len(words)
		for word_1 in words:
			if word_1 in stop_words:
				continue
			if word_1 not in cooccurence:
				cooccurence[word_1] = {}
			for word_2 in words:
				if word_2 in stop_words:
					continue
				if word_2 not in cooccurence[word_1]:
					cooccurence[word_1][word_2] = 0
				cooccurence[word_1][word_2] += 1
	f.close()

print('Building cooccurence matrix...')
vocabs = cooccurence.keys()
vocab_num = len(vocabs)
v_str_to_id = {}
v_id_to_str = {}
cooccur_matrix = np.zeros((vocab_num, vocab_num), dtype='float32')
vocab_id = 0
for v in vocabs:
	v_str_to_id[v] = vocab_id
	v_id_to_str[vocab_id] = v
	vocab_id += 1

for i in range(vocab_num):
	v1 = v_id_to_str[i]
	for j in range(vocab_num):
		v2 = v_id_to_str[j]
		print(i, j)
		try:
			c = cooccurence[v1][v2]
		except Exception:
			c = 1
		cooccur_matrix[i][j] = c
del cooccurence

print('Calculating PMI...')
Pall = np.sum(np.sum(cooccur_matrix))
Pi = np.sum(cooccur_matrix, 1) / Pall
Pj = np.sum(cooccur_matrix, 0) / Pall
Pij = cooccur_matrix / Pall

pmi = np.zeros((vocab_num, vocab_num), dtype='float32')
for i in range(vocab_num):
	pi = Pi[i]
	for j in range(vocab_num):
		pj = Pj[j]
		pij = Pij[i][j]
		try:
			pmi[i][j] = math.log( pij / (pi*pj), 2)
		except Exception:
			pmi[i][j] = -10000.0

print('Calculating mincontext...')
mincontext = np.zeros((vocab_num, vocab_num), dtype='float32')
sum_x_kj = np.sum(cooccur_matrix, 0)
sum_x_ik = np.sum(cooccur_matrix, 1)
for i in range(vocab_num):
	v1 = v_id_to_str[i]
	for j in range(vocab_num):
		v2 = v_id_to_str[j]
		mincontext[i][j] = min(sum_x_kj[j], sum_x_ik[i]) 

print('Calculating DMPI...')
delta = (cooccur_matrix / (cooccur_matrix + 1)) * (mincontext / mincontext + 1)
dpmi = pmi * dpmi

print('Saving DPMI Model...')
'''

'''