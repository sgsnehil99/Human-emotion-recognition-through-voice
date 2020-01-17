
!pip install -q keras

import keras
import os
import librosa
import librosa.display
import pandas as pd
import numpy as np
import sys
import glob

mylist= os.listdir('/content/drive/My Drive/Colab Notebooks/datasets')

type(mylist)
print(mylist[50])
print(mylist[50][6:-16])

data, sampling_rate=librosa.load('/content/drive/My Drive/Colab Notebooks/datasets/03-01-01-01-01-01-23.wav')
print(type(data))
print(type(sampling_rate))

import matplotlib
import matplotlib.pyplot as plt
plt.figure(figsize=(5,15))
librosa.display.waveplot(data,sr=sampling_rate)

import scipy.io.wavfile

##parameters
nstep= int(sampling_rate * 0.01)
nwin= int(sampling_rate * 0.03)
nfft=nwin

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

labels= pd.DataFrame(feeling_list)
labels

