import mysql.connector as mysql                    # for database communute.
import random
import quickstart
from passlib.hash import sha256_crypt
import numpy as np
import pandas as pd
import csv

class DataBase:
	def __init__(self,credsFileName="credential.txt"):
		with open(credsFileName,'r') as authCred:
			self.credentials=authCred.read().split('\n')
	def dbServerlogin(self):
		con=mysql.connect(host=self.credentials[0],user=self.credentials[1],password=self.credentials[2],database=self.credentials[3])
     # connection setup with our database.

		return con
	def executeQuery(self,con,query,val=(),ReturnMode=True):
		myCursor=con.cursor()
		if ReturnMode==True:		
			myCursor.execute(query,val)
			res=myCursor.fetchall()
			return res
		else:
			myCursor.execute(query,val)
			con.commit()
			return

class AuthLogin:
	def __init__(self):
		self.db=DataBase()
		self.con=self.db.dbServerlogin()
	def checkCredentials(self,userId,password):
		query=f"SELECT * FROM `users` WHERE `Name`='{userId}'"
		res=self.db.executeQuery(self.con,query)
		stat,msg,category=self.checkActiveStatus(userId)
		if(len(res)!=0 and sha256_crypt.verify(password,res[0][1])):
			return stat,res,msg,category
		else:
			return False,None,"Incorrect login credentials, please try again! ",'alert alert-danger'
	def checkActiveStatus(self,userId):
		query=f"SELECT * FROM `users` WHERE `Name`='{userId}' AND `activeStatus`=1"
		res=self.db.executeQuery(self.con,query)
		if len(res)!=0:
			return True,"You are successfully logged in!",'alert alert-success'
		else:
			return False,"Your account is not active, complete E-mail verification to activate your account!",'alert alert-danger'
		
		
class Registration:
	def __init__(self):
		self.db=DataBase()
		self.con=self.db.dbServerlogin()
	def registerUser(self,userId,password,email,profilePic):
		query="INSERT INTO `users`(`Name`,`Password`,`Mail`,`ProfilePic`,`userType`,`activeStatus`) VALUES(%s,%s,%s,%s,'user',0)"
		query1="SELECT * FROM `users` WHERE `Name`=%s OR `Mail`=%s"
		val=(userId,password,email,profilePic)
		val1=(userId,email)
		res=self.db.executeQuery(self.con,query1,val1)
		if len(res)!=0:
			return False
		else:
			self.db.executeQuery(self.con,query,val,ReturnMode=False)
			self.verificationLinkGenerator(userId)
			return True
	def verificationLinkGenerator(self,userName):
		query=f"SELECT `userId`,`Mail` FROM `users` WHERE `Name`='{userName}'"
		res=self.db.executeQuery(self.con,query)
		otp=random.randint(100000,999999)
		userId=res[0][0]
		query2=f"INSERT INTO `activation` VALUES({userId},{otp})"
		self.db.executeQuery(self.con,query2,ReturnMode=False)
		message_text=f"127.0.0.1:5000/activate?otp={otp}&userId={userId}  is your link. Either click it or paste it into your browser. \n\n Thanks & Regards,\nMed-desk\n\n This is a system generated mail."
		quickstart.driver("DigiDhan20@gmail.com", res[0][1], "Account Verification", message_text)
		return

	def updateProfile(self,val,mode,key):
		if mode=="1":
			query="UPDATE `users` SET `Password`=%s WHERE `userId`=%s"
			values=(val,key)
			self.db.executeQuery(self.con,query,values,ReturnMode=False)
		elif mode=="2":
			query="UPDATE `users` SET `Name`=%s WHERE `userId`=%s"
			values=(val,key)
			self.db.executeQuery(self.con,query,values,ReturnMode=False)
		else:
			query="UPDATE `users` SET `ProfilePic`=%s WHERE `userId`=%s"
			values=(val,key)
			self.db.executeQuery(self.con,query,values,ReturnMode=False)		

class otpValidator:
	def __init__(self):
		self.db=DataBase()
		self.con=self.db.dbServerlogin()
	def validate(self,otp,userId):
		query=f"SELECT * FROM `activation` WHERE `userId`={userId}"
		query1=f"UPDATE `users` SET `activeStatus`=1 WHERE `userId`={userId}"
		res=self.db.executeQuery(self.con,query)
		if(len(res)!=0):
			self.db.executeQuery(self.con,query1,ReturnMode=False)
			return True			
		else:
			return False
		
				
class chat:
	def __init__(self):
		self.db=DataBase()
		self.con=self.db.dbServerlogin()
	def post(self,to,From,msg,read_bit,ts):
		query="INSERT INTO `chat`(`to`,`from`,`message`,`read`,`timestamp`) VALUES(%s,%s,%s,%s,%s)"
		val=(to,From,msg,read_bit,ts)
		self.db.executeQuery(self.con,query,val=val,ReturnMode=False)
		return
	def get(self,uid):
		query=f"SELECT * FROM `chat` WHERE `to`={uid} OR `from`={uid}"
		res=self.db.executeQuery(self.con,query)
		query1=f"UPDATE `chat` SET `read`=1 WHERE `to`={uid} OR `from`={uid}"
		self.db.executeQuery(self.con,query1,ReturnMode=False)
		return res						

class csv_handler:
	def __init__(self,fname='hospital_data/hospital_data_min.csv'):
		self.fname=fname
	def getRecommendation(self,lat,lng,spec,n=3):
		# n is integer representing the number of recommendations provided.
		data=pd.read_csv(self.fname)
		min_idx=[]
		response=""
		lat_vals=data['Latitude'].values
		longi_vals=data['Longitude'].values
		specialization=data['Specialisation'].values
		n_beds=data['n_beds'].values
		for n_recs in range(n):
			temp_idx=0
			min_diff=99999
			for i in range(len(lat_vals)):
				if(i not in min_idx) and (int(n_beds[i])>0) and (spec.lower() in specialization[i].lower()) :
					distance=((float(lat) - float(lat_vals[i]))**2 + (float(lng) - float(longi_vals[i]))**2)**0.5
					if  distance < min_diff:
						min_diff=distance
						temp_idx=i
			min_idx.append(temp_idx)
			response+=f"Found <i> {n_recs + 1}. {data['Hospital_Name'].values[min_idx[n_recs]]}</i> which is situated in <i>{data['Location'].values[min_idx[n_recs]]}, {data['District'].values[min_idx[n_recs]]}, {data['State'].values[min_idx[n_recs]]}-{data['Pincode'].values[min_idx[n_recs]]} having {n_beds[min_idx[n_recs]]} beds with specialization in {specialization[min_idx[n_recs]]}</i>" 
			response+='. Click <a href="/map?lat='+str(lat_vals[min_idx[n_recs]])+'&lng='+str(longi_vals[min_idx[n_recs]])+'">here</a> to view on map <br>'
		return response
	def append_csv(self,data):
		with open(self.fname,'a') as file:
			writer=csv.writer(file)
			writer.writerow(data)
		return True
	def delete_csv(self,data):
		df=pd.read_csv(self.fname)
		idx=[]
		loc=df['Location'].values
		name=df['Hospital_Name'].values
		stt=df['State'].values
		dist=df['District'].values
		pin=df['Pincode'].values
		lat=df['Latitude'].values
		lng=df['Longitude'].values
		spec=df['Specialisation'].values
		n_beds=df['n_beds'].values
		# loc,name,stt,dist,pin,lat,lng
		for i in range(len(dummy)):
			if(loc[i]==data[0] and name[i]==data[1] and stt[i]==data[2] and dist[i]==data[3] and pin[i]==data[4] and lat[i]==data[5] and lng[i]==data[6] and spec==data[7] and n_beds==data[8]):
				idx.append(i)
		if len(idx)!=0:
			df=df.drop(idx)
			df=df.reset_index(drop=True)
			df.to_csv(self.fname,index=False)
			return True
		else:
			return False

	def getData(self):
		df=pd.read_csv(self.fname)
		return df.values.tolist()
			

class user_data:
	def __init__(self):
		self.db=DataBase()
		self.con=self.db.dbServerlogin()
	def getUserData(self):
		query="SELECT `userId`,`Name`,`Mail`,`ProfilePic`,`activeStatus` FROM `users` WHERE `userType`='user'"
		res=self.db.executeQuery(self.con,query)
		return res
			
class activation_handler:
	def __init__(self):
		self.db=DataBase()
		self.con=self.db.dbServerlogin()
	def activate(self,uid):
		query=f"UPDATE `users` SET `activeStatus`=1 WHERE `userId`={uid}"
		self.db.executeQuery(self.con,query,ReturnMode=False)
		return True
	def deactivate(self,uid):
		query=f"UPDATE `users` SET `activeStatus`=0 WHERE `userId`={uid}"
		self.db.executeQuery(self.con,query,ReturnMode=False)
		return True

'''class State_wise_facility:
	def __init__(self, fname='hospital_data/state_wise_facility_links.csv'):
		self.fname = fname

	def get_data(self):
		df=pd.read_csv(self.fname)
		return df.values.tolist()'''