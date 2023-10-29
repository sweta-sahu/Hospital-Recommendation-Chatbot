#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ChatBot_Utility as bot


# In[2]:


bot.warnings.filterwarnings('ignore')


def respond(fName):
	with open(fName,"r") as file:
		data1=bot.json.load(file)
	with open("intents.json","r") as file:
		data2=bot.json.load(file)
	X, userIds=bot.inputPreprocessing(data1,data2)
	X=bot.np.array(X)
	with open("tags.json",'r') as file:
		data=bot.json.load(file)
	model=bot.Model(100,16,30,10,fname='model.h5')
	model.load_model('model.h5')
	preds=model.predict(X)
	res=[]
	for i in preds:
		for j in data2['intents']:
			if j['tag']==data[str(bot.np.argmax(i))]:
				res.append([j['responses'][bot.random.randint(0,len(j['responses'])-1)],j['action']])
	response_dict={"responses" : [],"userID" : [],"action" : []}
	for i in res:
		response_dict["responses"].append(i[0])
		response_dict["action"].append(i[1])
		response_dict["userID"]=userIds
	with open(fName,'w') as file:
		bot.json.dump(response_dict,file)
	return



