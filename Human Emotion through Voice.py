!pip install -q keras

from keras.layers.normalization import BatchNormalization
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from matplotlib.pyplot import specgram
import keras
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Input, Flatten, Dropout, Activation
from keras.layers import Conv1D, MaxPooling1D, AveragePooling1D
from keras.models import Model
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import confusion_matrix
import sys
import glob
import os

mylist= os.listdir('/content/drive/My Drive/DATASET/datasets')

type(mylist)
print(mylist[50])
print(mylist[50][6:-16])

data, sampling_rate=librosa.load('/content/drive/My Drive/DATASET/datasets/03-01-01-01-01-01-05.wav')
print(type(data))
print(type(sampling_rate))

import matplotlib
import matplotlib.pyplot as plt
plt.figure(figsize=(5,15))
librosa.display.waveplot(data,sr=sampling_rate)

import scipy.io.wavfile

##parameters
x, sampling_rate=librosa.load('/content/drive/My Drive/DATASET/datasets/03-01-01-01-01-01-05.wav')
nstep= int(sampling_rate * 0.01)
nwin= int(sampling_rate * 0.03)
nfft=nwin

window = np.hamming(nwin)
nn = range(nwin, len(x), nstep)
X= np.zeros((len(nn), nfft//2))

feeling_list=[]
for item in mylist:
    if item[6:-16]=='02' and int(item[18:-4])%2==0:
        feeling_list.append('female_calm')
    elif item[6:-16]=='02' and int(item[18:-4])%2==1:
        feeling_list.append('male_calm')
    elif item[6:-16]=='03' and int(item[18:-4])%2==0:
        feeling_list.append('female_happy')
    elif item[6:-16]=='03' and int(item[18:-4])%2==1:
        feeling_list.append('male_happy')
    elif item[6:-16]=='04' and int(item[18:-4])%2==0:
        feeling_list.append('female_sad')
    elif item[6:-16]=='04' and int(item[18:-4])%2==1:
        feeling_list.append('male_sad')
    elif item[6:-16]=='05' and int(item[18:-4])%2==0:
        feeling_list.append('female_angry')
    elif item[6:-16]=='05' and int(item[18:-4])%2==1:
        feeling_list.append('male_angry')
    elif item[6:-16]=='06' and int(item[18:-4])%2==0:
        feeling_list.append('female_fearful')
    elif item[6:-16]=='06' and int(item[18:-4])%2==1:
        feeling_list.append('male_fearful')

import pandas as pd
labels= pd.DataFrame(feeling_list)
labels

df = pd.DataFrame(columns=['features'])
bookmark=0
for index, y in enumerate(mylist):
  if mylist[index][6:-16]!='01' and mylist[index][6:-16]!='07' and mylist[index][6:-16]!='08' :
    X, sample_rate = librosa.core.load('/content/drive/My Drive/DATASET/datasets/' +y,res_type='kaiser_fast', duration=2.5, sr=22050*2, offset=0.5)
    sample_rate = np.array(sample_rate)
    mfccs=np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13), axis=0)
    feature = mfccs
    df.loc[bookmark]= [feature]
    bookmark=bookmark+1

type(df)
df.columns

df3 = pd.DataFrame(df['features'].values.tolist())

newdf = pd.concat([df3, labels], axis=1)

rnewdf = newdf.rename(index=str, columns={"0": "label"})

rnewdf[:5]

from sklearn.utils import shuffle
rnewdf = shuffle(newdf)
rnewdf[:5]

rnewdf = rnewdf.fillna(0)
type(rnewdf)

newdf1 = np.random.rand(len(rnewdf)) < 0.8
train = rnewdf[newdf1]
test = rnewdf[~newdf1]

train[250:260]

trainfeatures = train.iloc[:, :-1]
trainlabel = train.iloc[:, -1:]
testfeatures = test.iloc[:, :-1]
testlabel = test.iloc[:, -1:]

from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder

x_train = np.array(trainfeatures)
y_train = np.array(trainlabel)
x_test = np.array(testfeatures)
y_test = np.array(testlabel)

lb = LabelEncoder()

y_train = np_utils.to_categorical(lb.fit_transform(y_train))
y_test = np_utils.to_categorical(lb.fit_transform(y_test))

x_train.shape

x_traincnn = np.expand_dims(x_train, axis=52)
x_testcnn = np.expand_dims(x_test, axis=2)

model = Sequential()

model.add(Conv1D(256, 5, padding='same', input_shape=(216,1)))
model.add(Activation('relu'))

model.add(Conv1D(128, 5, padding='same'))
model.add(Activation('relu'))

model.add(Dropout(0.5))
model.add(MaxPooling1D(pool_size=(8)))
model.add(Conv1D(128, 5, padding='same'))
model.add(Activation('relu'))
model.add(Conv1D(128, 5, padding='same'))
model.add(Activation('relu'))

model.add(Flatten())
model.add(Dense(10))
model.add(Activation('softmax'))
opt = keras.optimizers.rmsprop(lr=0.00001, decay=1e-6)

model.summary()

model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

cnnhistory=model.fit(x_traincnn, y_train, batch_size=16, epochs=1000, validation_data=(x_testcnn, y_test))

#cnnhistory=model.fit(x_traincnn, y_train, batch_size=16, epochs=700, validation_data=(x_testcnn, y_test))

os.chdir('/content/drive/My Drive/Colab Notebooks')

os.getcwd()

plt.plot(cnnhistory.history['loss'])
plt.plot(cnnhistory.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

model_name = 'Emotion_Voice_Detection_Model.h5'
save_dir = os.path.join(os.getcwd(), 'saved_models')
# Save model and weights
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)
model_path = os.path.join(save_dir, model_name)
model.save(model_path)
print('Saved trained model at %s ' % model_path)

import json
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

# loading json and creating model
from keras.models import model_from_json
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("saved_models/Emotion_Voice_Detection_Model.h5")
print("Loaded model from disk")
 
# evaluate loaded model on test data
loaded_model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
score = loaded_model.evaluate(x_testcnn, y_test, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))

preds = loaded_model.predict(x_testcnn, 
                         batch_size=32, 
                         verbose=1)

preds

preds1=preds.argmax(axis=1)

preds1

abc = preds1.astype(int).flatten()
abc

predictions = (lb.inverse_transform((abc)))

preddf = pd.DataFrame({'predictedvalues': predictions})
preddf[:10]

actual=y_test.argmax(axis=1)
abc123 = actual.astype(int).flatten()
actualvalues = (lb.inverse_transform((abc123)))

actualdf = pd.DataFrame({'actualvalues': actualvalues})
actualdf[:10]

finaldf = actualdf.join(preddf)

finaldf[170:180]

finaldf.groupby('actualvalues').count()

finaldf.groupby('predictedvalues').count()

finaldf.to_csv('Predictions.csv', index=False)

#demo
data, sampling_rate = librosa.load('/content/drive/My Drive/DATASET/datasets/03-01-01-01-01-01-22.wav')

# Commented out IPython magic to ensure Python compatibility.
# % pylab inline
import os
import pandas as pd
import librosa
import glob

plt.figure(figsize=(15,5))
librosa.display.waveplot(data, sr=sampling_rate)

X, sample_rate = librosa.load('/content/drive/My Drive/DATASET/datasets/03-01-01-01-01-01-22.wav', res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
sample_rate = np.array(sample_rate)
mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
featurelive = mfccs
livedf2 = featurelive

livedf2= pd.DataFrame(data=livedf2)

livedf2 = livedf2.stack().to_frame().T

livedf2

twodim= np.expand_dims(livedf2, axis=2)

livepreds = loaded_model.predict(twodim, 
                         batch_size=32, 
                         verbose=1)

livepreds1=livepreds.argmax(axis=1)

liveabc = livepreds1.astype(int).flatten()

livepredictions = (lb.inverse_transform((liveabc)))
livepredictions

