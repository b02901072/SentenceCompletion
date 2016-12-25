import numpy as np
import IO


# vecDict = IO.readVec("data/train_vectors.10.txt")
# vocabDict = IO.readVocab("data/train_vectors.10.txt")

# timesteps = 15
# data_dim = 200
# N = 200

def test(file, vecDict):
    x = IO.readSentVec( file, vecDict, False )
    y = x
    for i in y:
        i = i[2:]
    for i in x:
        i = i[1:-1]
    
    ansList = []
    scoreList = []
    for i in range( len( x ) ):
        y_pred = model.predict( x[i] )
        # print "y_pred", y_pred
        score = 0
        for j in y_pred :
            # print "j", np.dtype( j )
            jscore = -1
            simscore = 0
            for k in vecDict.values():
                # print "k", np.dtype( k )
                simscore = np.dot( j, k ) / np.sqrt( np.sum( np.square( j ) ) * np.sum( np.square( k ) ) )
                if simscore > jscore:
                    # print simscore
                    jscore = simscore
            score += jscore
        scoreList.append( score )
        # print "i", i
        # print len( scoreList )
        if i % 5 == 4 :
            ansN = 0
            ans = scoreList[0]
            # print len( scoreList )
            for j in range(5):
                # print scoreList[j]
                if scoreList[j] > ans :
                    ansN = j
                    ans = scoreList[j]
            ansList.append( ansN )
            print ansN
            scoreList = []

# print "test"
# test("data/testing/Data/Holmes.lm_format.questions.txt")

