#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Bidirectional, Dropout, Embedding, Flatten
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import MeanSquaredError as mse
import random
import warnings
import pandas as pd
import json
import os


# In[2]:


class Tokenize:
    def __init__(self,num_words=None):
        self.num_words=num_words
        if num_words!=None:
            self.tokenizer=Tokenizer(num_words=self.num_words)
        else:
            self.tokenizer=Tokenizer()
    def fit(self,words):
        self.tokenizer.fit_on_texts(words)
    def getSequences(self,inputs):
        return self.tokenizer.texts_to_sequences(inputs)
    def padSequences(self,seq,maxlen=30,padding='pre'):
        return pad_sequences(seq,maxlen=maxlen,padding=padding)


# In[3]:


class Model:
    def __init__(self,vocab_size,embedding_dim,input_length,output_classes,fname=None):
        if fname!=None:
            self.load_model(fname) 
        else:
            self.model=Sequential()
            self.model.add(Embedding(vocab_size+1,embedding_dim,input_length=input_length))
            self.model.add(LSTM(256,return_sequences=True,activation='relu'))
            self.model.add(LSTM(128,return_sequences=True,activation='relu'))
            self.model.add(LSTM(64,return_sequences=True,activation='relu'))
            self.model.add(LSTM(32,return_sequences=True,activation='relu'))
            self.model.add(LSTM(16,activation='relu'))
            self.model.add(Flatten())
            self.model.add(Dense(16,activation='relu'))
            self.model.add(Dense(output_classes,activation='softmax'))
            self.model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy',mse()])
            ################################################################################################################################
    def save_model(self,fname):
        self.model.save(fname)
        return
    def load_model(self,fname):
        assert os.path.exists(fname)==True , f"{fname} model file should exist!"
        self.model=load_model(fname)
        return
    def fit(self,X,Y,batch_size,epochs):
        self.model.fit(X,Y,batch_size=batch_size,epochs=epochs)
        return
    def predict(self,X):
        return self.model.predict(X)


# In[4]:


tokenizer=Tokenize()
stop_symbols=['.','!',',','?','\'','&']


# In[5]:


def jsonifyTags(tags):
    tag_dict={i : tags[i] for i in range(len(tags))}
    with open("tags.json",'w') as tagFile:
        json.dump(tag_dict,tagFile)
    return


# In[6]:


def intentPreprocessing(data,padding_len=30,padding_mode='pre'):
    words=[]
    n_tags=0
    tags=[]
    inputs=[]
    Y=[]
    for intent in data['intents']:
        for header in intent.keys():
            temp=intent[header]
            if header=='tag':
                tags.append(intent[header])
                n_tags+=1
            if type(temp)==type([]):
                for i in temp:
                    if i not in words:
                        words.append(i.lower())
            else:
                if temp not in words:
                    words.append(temp.lower())
    words.remove('')
    for i in words:
        for j in stop_symbols:
            i.replace(j,'')
    tokenizer.fit(words)
    for intent in data['intents']:
        for pattern in intent['pattern']:
            temp=np.zeros((n_tags))
            pattern=pattern.lower()
            for j in stop_symbols:
                pattern=pattern.replace(j,'')
            inputs.append(pattern)
            temp[tags.index(intent['tag'])]=1
            Y.append(temp)
    pattern_sequence=tokenizer.getSequences(inputs)
    X=tokenizer.padSequences(pattern_sequence,maxlen=padding_len,padding=padding_mode)   # assumption : 30 is the input word limit. (can be changed)
    word_indexes=tokenizer.tokenizer.word_index
    jsonifyTags(tags)
    return(X,Y,len(word_indexes),n_tags,padding_len)


# In[7]:


def inputPreprocessing(data1,data2,padding_len=30,padding_mode='pre'):
    X=[]
    words=[]
    n_tags=0
    tags=[]
    inputs=[]
    Y=[]
    userIds=[]
    for intent in data2['intents']:
        for header in intent.keys():
            temp=intent[header]
            if header=='tag':
                tags.append(intent[header])
                n_tags+=1
            if type(temp)==type([]):
                for i in temp:
                    if i not in words:
                        words.append(i.lower())
            else:
                if temp not in words:
                    words.append(temp.lower())
    words.remove('')
    for i in words:
        for j in stop_symbols:
            i.replace(j,'')
    tokenizer.fit(words)
    for inps in data1['inputs']:
        inputs=inps['in']
        userIds.append(inps['userID'])
        inputs=inputs.lower()
        for j in stop_symbols:
            inputs=inputs.replace(j,'')
        X.append(inputs)
    pattern_sequence=tokenizer.getSequences(X)
    X=tokenizer.padSequences(pattern_sequence,maxlen=padding_len,padding=padding_mode)   # assumption : 30 is the input word limit. (can be changed)
    return X, userIds


# In[ ]:



