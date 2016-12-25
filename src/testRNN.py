from keras.models import Sequential, model_from_json
from keras.layers import LSTM
from keras.layers.core import Dense, Activation
import numpy as np

data_dim = 200
timesteps = 15
out_dim = 200

# expected input data shape: (batch_size, timesteps, data_dim)
print "model = Sequential()"
model = Sequential()
print "model.add(LSTM(512, return_sequences=True, input_shape=(timesteps, data_dim)))"
model.add(LSTM(512, return_sequences=True,
               input_shape=(timesteps, data_dim)))  # returns a sequence of vectors of dimension 32
print "model.add(LSTM(32, return_sequences=True))"
model.add(LSTM(32, return_sequences=True))  # returns a sequence of vectors of dimension 32
print "model.add(LSTM(out_dim, return_sequences=True))"
model.add(LSTM(out_dim, return_sequences=True))  # returns a sequence of vectors of dimension 32
print "model.add(Activation('softmax'))"
model.add(Activation('softmax'))

print "model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])"
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# generate dummy training data
x_train = np.random.random((1000, timesteps, data_dim))
y_train = np.random.random((1000, timesteps, out_dim))

x_test = np.random.random((100, timesteps, data_dim))
# generate dummy validation data
# x_val = np.random.random((100, timesteps, data_dim))
# y_val = np.random.random((100, timesteps, out_dim))

print "fit 1"
model.fit(x_train, y_train,
          batch_size=64, nb_epoch=5)#,
          # validation_data=(x_val, y_val))

y1 = model.predict(x_test) 

print "save json"
with open("model/model.json" , 'w') as f:
    f.write(model.to_json())

print "save h5"
model.save_weights("model/model_weights.h5")

print "load json"
with open("model/model.json", "r+") as f:
    model = model_from_json(f.read())

print "load h5"
model.load_weights("model/model_weights.h5")

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

y2 = model.predict(x_test)
print "predicted"
if y1 == y2:
    print "true"
else:
    print "false"

# print "fit 2"
# model.fit(x_train, y_train,
          # batch_size=64, nb_epoch=5)#,
          # validation_data=(x_val, y_val))
