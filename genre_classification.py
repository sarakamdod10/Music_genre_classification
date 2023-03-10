import os
for dirname, _, filenames in os.walk('/content/Music'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import scipy
import os
import pickle
import librosa
import librosa.display
from IPython.display import Audio
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow import keras

df = pd.read_csv('/content/Music/features_3_sec.csv')
df.head()

df.shape

df.dtypes

df=df.drop(labels="filename",axis=1)

Understanding the audio files

audio_recording="/content/Music/country.00000.wav"
data,sr=librosa.load(audio_recording)
print(type(data),type(sr))

librosa.load(audio_recording,sr=45600)

import IPython
IPython.display.Audio(data,rate=sr)

Visualising audio files

plt.figure(figsize=(12,4))
librosa.display.waveplot(data,color="#2B4F72")
plt.show()

stft=librosa.stft(data)
stft_db=librosa.amplitude_to_db(abs(stft))
plt.figure(figsize=(14,6))
librosa.display.specshow(stft,sr=sr,x_axis='time',y_axis='hz')
plt.colorbar()

stft=librosa.stft(data)
stft_db=librosa.amplitude_to_db(abs(stft))
plt.figure(figsize=(14,6))
librosa.display.specshow(stft_db,sr=sr,x_axis='time',y_axis='hz')
plt.colorbar()

spectral_rolloff=librosa.feature.spectral_rolloff(data+0.01,sr=sr)[0]
plt.figure(figsize=(14,6))
librosa.display.waveplot(data,sr=sr,alpha=0.4,color="#2B4F72")

import librosa.display as lplt
chroma = librosa.feature.chroma_stft(data,sr=sr)
plt.figure(figsize=(14,6))
lplt.specshow(chroma,sr=sr,x_axis="time",y_axis="chroma",cmap="coolwarm")
plt.colorbar()
plt.title("Chroma Features")
plt.show()

Zero Crossing Rate

start=1000
end=1200
plt.figure(figsize=(12,4))
plt.plot(data[start:end],color="#2B4F72")
plt.grid()

zero_cross_rate=librosa.zero_crossings(data[start:end],pad=False)
print("the numbert of zero_crossings is :", sum(zero_cross_rate))

Feature Extraction

class_list=df.iloc[:,-1]
converter=LabelEncoder()

y=converter.fit_transform(class_list)
y

print(df.iloc[:,:-1])

Scaling the features

from sklearn.preprocessing import StandardScaler
fit=StandardScaler()
X=fit.fit_transform(np.array(df.iloc[:,:-1],dtype=float))

Dividing Training and Testing Dataset

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.33)

len(y_test)

len(y_train)

![37549simple_result.png](data:image/png;base64,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)

Building the model

from tensorflow.keras.models import Sequential

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier, XGBRFClassifier
from xgboost import plot_tree, plot_importance

from sklearn.metrics import confusion_matrix, accuracy_score, roc_auc_score, roc_curve
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE

model = keras.Sequential([keras.layers.Dense(10, activation='sigmoid')])

model.compile(
               optimizer='adam', 
               loss='sparse_categorical_crossentropy', 
               metrics=['accuracy'])

model.fit(X_train, y_train, epochs = 40)

model.evaluate(X_test, y_test)

def trainModel(model,epochs,optimizer):
    batch_size=128
    model.compile(optimizer=optimizer,loss='sparse_categorical_crossentropy',metrics='accuracy')
    return model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=epochs,batch_size=batch_size)

def plotValidate(history):
    print("Validation Accuracy",max(history.history["val_accuracy"]))
    pd.DataFrame(history.history).plot(figsize=(12,6))
    plt.show()

model=tf.keras.models.Sequential([
    tf.keras.layers.Dense(512,activation='relu',input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dropout(0.2),
    
    tf.keras.layers.Dense(256,activation='relu'),
    keras.layers.Dropout(0.2),
    
    tf.keras.layers.Dense(128,activation='relu'),
    tf.keras.layers.Dropout(0.2),
    
    tf.keras.layers.Dense(64,activation='relu'),
    tf.keras.layers.Dropout(0.2),
    
    tf.keras.layers.Dense(10,activation='softmax'),
])

print(model.summary())
model_history=trainModel(model=model,epochs=600,optimizer='adam')

test_loss,test_acc=model.evaluate(X_test,y_test,batch_size=128)
print("The test loss is ",test_loss)
print("The best accuracy is: ",test_acc*100)

y, sr = librosa.load(f'/content/Music/country.00000.wav')

print('y:', y, '\n')
print('y shape:', np.shape(y), '\n')
print('Sample Rate (KHz):', sr, '\n')

# Verify length of the audio
print('Check Len of Audio:', 661794/22050)

audio_file, _ = librosa.effects.trim(y)

# the result is an numpy ndarray
print('Audio File:', audio_file, '\n')
print('Audio File shape:', np.shape(audio_file))

zero_crossings = librosa.zero_crossings(audio_file, pad=False)
print(sum(zero_crossings))

Beats per Minute

tempo, _ = librosa.beat.beat_track(y, sr = sr)
tempo
