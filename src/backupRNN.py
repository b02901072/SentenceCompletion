from keras.models import Sequential, model_from_json
from keras.layers import Dense, Activation, SimpleRNN
from keras import backend as K
import numpy as np
import IO
import tryBackupTest

vectorFile = "data/train_vectors.10.txt"
trainQFile = "data/data.TXT.punc.word.fit.input"
trainAFile = "data/data.TXT.punc.word.fit.output"
testFile = "data/testing/Data/Holmes.lm_format.questions.txt"
modelJson = "model/model.json"
modelH5 = "model/model_weights.h5"

vecDict = IO.readVec( vectorFile )
# vocabDict = IO.readVocab( vectorFile )
vecMatrix = K.variable( np.array( vecDict.values() ), name="vecMatrix" ) 

timesteps = 40
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
    A
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
    A
    l = 0
    for i in range( timesteps ):
        for j in range( len( vecDict ) ) :
            if K.equal( vecMatrix[j], y_true[i] ):
                l += softmax[j, i]
                break
    # print "l", K.shape( softmax[j, i] ).eval()
    return l

# model.compile(loss='mae',
print "model.compile(loss=cost, optimizer='rmsprop', metrics=['accuracy'])"
model.compile(loss='mae',
              optimizer='rmsprop',
              metrics=['accuracy'])

x = np.array(IO.readSentVec( trainQFile, vecDict, False ))
y = np.array(IO.readSentVec( trainAFile, vecDict, False ))
print "x,", x.shape
print "y,", y.shape

print "model.fit(x, y, batch_size=1, nb_epoch=10)"
model.fit(x, y,
          batch_size=1, nb_epoch=10)

with open( modelJson , 'w' ) as f:
    f.write( model.to_json() )

model.save_weights( modelH5 )

# with open("model/model.json", "r+") as f:
    # model = model_from_json(f.read())

# model.load_weights("model/model_weights.h5")

print "test"
tryBackupTest.test( testFile, vecDict )

