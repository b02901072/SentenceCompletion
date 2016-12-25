from keras.models import Sequential
from keras.layers import Dense, Activation, SimpleRNN
from keras import backend as K
import numpy as np
import IO


vecDict = IO.readVec("data/train_vectors.10.txt")
vocabDict = IO.readVocab("data/train_vectors.10.txt")
vecMatrix = K.variable( np.array( vecDict.values() ), name="vecMatrix" ) 

timesteps = 15
data_dim = 200
N = 200

print "model = Sequential()"
model = Sequential()
print "model.add(SimpleRNN(512, return_sequences=True, input_shape=(timesteps, data_dim)))"
model.add(SimpleRNN(512, return_sequences=True,
                    input_shape=(timesteps, data_dim)))
print "model.add(SimpleRNN(32, return_sequences=True))"
model.add(SimpleRNN(32, return_sequences=True))
print "model.add(SimpleRNN(N, return_sequences=True))"
model.add(SimpleRNN(N, return_sequences=True))

def similar(M, v):
    s = K.dot( v, K.transpose( M ) )
    lenM = K.sqrt( K.sum( K.square( M ), axis=1, keepdims=False ) )
    lenv = K.sqrt( K.sum( K.square( v ), axis=1, keepdims=False ) )
    s = s / K.dot( lenM, lenv )
    return s


def cost(y_true, y_pred):
    # print "similar"
    # print "M", K.shape( vecMatrix ).eval()
    Sims = similar( y_pred, vecMatrix )
    softmax = K.exp( Sims ) / K.sum( K.exp( Sims ), axis=1, keepdims=False )
    l = K.variable( 0 )
    for i in range( timesteps ):
        for j in range( len( vecDict ) ) :
            if K.equal( vecMatrix[j], y_true[i] ):
                l += softmax[j, i]
                break
    # print "l", K.shape( softmax[j, i] ).eval()
    return l

# model.compile(loss='mae',
print "model.compile(loss=cost, optimizer='rmsprop', metrics=['accuracy'])"
model.compile(loss=cost,
              optimizer='rmsprop',
              metrics=['accuracy'])

# x = np.array(IO.readSentVec("data/input/04TOM10.TXT", vecDict))
x = np.array(IO.readSentVec("data/data.TXT.punc.word.input", vecDict, False))
y = np.array(IO.readSentVec("data/data.TXT.punc.word.output", vecDict, False))
# y = np.array(IO.readSentVocab("data/output/04TOM10.TXT", vocabDict))
# y = np.array(IO.readSentVocabVec("data/data.TXT.punc.word.output", vocabDict))
print "x,", x.shape
print "y,", y.shape

print "model.fit(x, y, batch_size=1, nb_epoch=10)"
model.fit(x, y,
          batch_size=1, nb_epoch=10)

def test(file):
    x = IO.readSentVec( file, vecDict )
    y = x
    for i in y:
        i = i[1:]
    for i in x:
        i = i[:-1]
    
    ansList = []
    for i in range( len( x ) ):
        y_pred = model.predict( np.array( x[i] ) )
        scoreList = []
        score = 0
        for j in y_pred :
            jscore = -1
            for k in vecDict.values():
                simscore = np.dot( j, k ) / np.sqrt( np.dot( j, j ) * np.dot( k, k ) )
                if simscore > jscore:
                    jscore = simscore
            score += jscore
        scoreList.append( score )
        if i % 5 == 4 :
            ansN = 0
            ans = scoreList[0]
            for j in range(5):
                if scoreList[j] > ans :
                    ansN = j
                    ans = scoreList[j]
            ansList.append( ansN )
            print ansN

print "test"
test("data/testing/Data/Holmes.lm_format.questions.txt")

