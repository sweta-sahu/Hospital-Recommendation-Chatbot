#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ChatBot_Utility as bot


# In[2]:


bot.warnings.filterwarnings('ignore')


# In[3]:

with open("intents.json","r") as file:
    	data=bot.json.load(file)


# In[4]:


X,Y,vocab_size,n_classes,input_len=bot.intentPreprocessing(data)


# In[5]:


X=bot.np.array(X)
Y=bot.np.array(Y)


# In[6]:


if bot.os.path.exists('model.h5'):
    	fname='model.h5'
else:
    	fname=None
model=bot.Model(vocab_size,16,input_length=input_len,output_classes=n_classes,fname=fname)


# In[7]:


model.fit(X,Y,batch_size=8,epochs=200)


# In[8]:


model.save_model('model.h5')

