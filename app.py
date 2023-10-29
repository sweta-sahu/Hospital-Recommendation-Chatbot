from flask import Flask,request,redirect,url_for,session,flash,render_template
import database
import ChatBot_Utility as bot
import ChatBot_Inference as engine 
#import ChatBot_Train as Trainer
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename   # secured file upload
from datetime import datetime
import gmaps
from ipywidgets.embed import embed_minimal_html
app=Flask(__name__)
app.secret_key='QwErTY9934@123'
gmaps.configure(api_key='AIzaSyDFHxoMv_gH0mb-tgxpRs7k-doEx8l-jKU')
@app.route('/')
def HomePage():
	return render_template('index.html')
@app.route('/register')
def register():
	return render_template('register.html')	
@app.route('/login')
def login():
	return render_template('login.html')
@app.route('/registerBack',methods=['POST'])
def registerBack():
	registrar=database.Registration()
	if request.method=='POST':
		userId=request.form['userId']
		password=sha256_crypt.encrypt(request.form['password'])
		email=request.form['email']
		profilePic=request.files['profilePic']
		fileName=userId + secure_filename(profilePic.filename)
		profilePic.save('static/PROFILE_PIC/'+fileName)
	else:
		flash("Unsupported method of registration! Please use the registration tab instead.",'alert alert-danger')
		return redirect(url_for("HomePage"))
	profilePath='static/PROFILE_PIC/'+fileName
	res=registrar.registerUser(userId,password,email,profilePath)
	print(res)
	if res==True:
		# as we advance, incorporate functionality of OTP verification as well.
		flash("You are successfully registered! verification link has been sent to your registered E-mail.",'alert alert-success') 
		return redirect(url_for('login'))
	else:
		flash("User with provided data already exists! ",'alert alert-danger')
		return redirect(url_for('register'))

@app.route('/loginBack',methods=['POST'])
def loginBack():
	authenticator=database.AuthLogin()
	if request.method=='POST':
		userId=request.form['userId']
		password=request.form['password']
	else:
		flash("Unsupported method of login! Please use the login tab instead.",'alert alert-danger')
		return redirect(url_for("HomePage"))
	status,res,msg,category=authenticator.checkCredentials(userId,password)
	flash(msg,category)
	if status==True:
		session['username']=res[0][0]
		session['email']=res[0][2]
		session['profilePic']=res[0][3]
		session['type']=res[0][6]
		session['userId']=res[0][4]
		return redirect(url_for('HomePage'))
	else:
		return redirect(url_for('login'))

@app.route('/logout')
def logout():
	flash('You are successfully logged out!','alert alert-success')
	session.pop('username',None)
	session.pop('email',None)
	session.pop('profilePic',None)
	return redirect(url_for('HomePage'))

@app.route('/admin')
def admin():
	return render_template('admin.html')
@app.route('/messenger')
def messenger():
	return render_template('messenger.html')
@app.route('/settings')
def settings():
	return render_template('settings.html')

@app.route('/ventures')
def ventures():
	return render_template('ventures.html')

@app.route('/state_wise_covid19_facility')
def covid():
	return render_template('state_wise_facility.html')

@app.route('/activate')
def activate():
	otp = request.args.get('otp')
	userId=request.args.get('userId')
	otpVal=database.otpValidator()
	if otpVal.validate(otp,userId)==True:
		flash("Congratulations! Your account has been activated. Try logging in.",'alert alert-success')
		return redirect(url_for('login'))
	else:
		flash("OTP verification Failed! Try again later.",'alert alert-danger')
		return redirect(url_for('HomePage'))		
@app.route('/chat_post',methods=['GET'])
def chat_post():
	chat=database.chat()
	data={"inputs" : []}
	if request.method=='GET':
		data["inputs"].append({"in" : request.args.get('msg'),"userID" : session['userId'],"action" : ""})
		uid=session["userId"]
		with open(f"{uid}.json",'w') as file:
			bot.json.dump(data,file)
		now=datetime.now()
		ts=now.strftime("%d/%m/%Y %H:%M:%S")
		msg=request.args.get('msg')
		chat.post(0,session['userId'],msg,0,ts)
		engine.respond(f"{uid}.json")   # it will make inference and create response.json file.
		with open(f"{uid}.json",'r') as file:
			data=bot.json.load(file)
		now=datetime.now()
		ts=now.strftime("%d/%m/%Y %H:%M:%S")
		chat.post(session['userId'],0,data['responses'][0],0,ts)
		if len(data['action'][0])>0:
			# perform recommendation and plot the recommendation on the map.
			# https://medium.com/future-vision/google-maps-in-python-part-2-393f96196eaf
			csv_hndl=database.csv_handler()
			res=csv_hndl.getRecommendation(session['latitude'],session['longitude'],data['action'][0])
			now=datetime.now()
			ts=now.strftime("%d/%m/%Y %H:%M:%S")
			chat.post(session['userId'],0,res,0,ts)
@app.route('/chat_fetch',methods=['GET'])
def chat_fetch():
	chat=database.chat()
	if request.method=='GET':
		uid=session["userId"]
		response=''
		res=chat.get(uid)
		for i in res:
			if i[0]==uid:
				response+='<br><div class="message1">'+i[2]+'<br><font color="gray">'+i[4]+'</font><br></div><br>' 
			elif i[1]==uid:
				response+='<br><div class="message2">'+i[2]+'<br><font color="gray">'+i[4]+'</font><br></div><br>'
		return response
		
@app.route('/storePosition',methods=['GET'])
def storePosition():
	if request.method=='GET':
		session['latitude']=request.args.get('lat')
		session['longitude']=request.args.get('longi')	
		

@app.route('/map',methods=['GET'])
def map():
	if request.method=='GET':
		myLoc=(float(session['latitude']),float(session['longitude']))
		hospital=(float(request.args.get('lat')),float(request.args.get('lng')))
		fig = gmaps.figure()
		layer = gmaps.directions.Directions(myLoc, hospital,mode='car')
		fig.add_layer(layer)
		uid=session['userId']
		name=f"{uid}.html"
		embed_minimal_html("templates/"+name, views=[fig])
		return render_template(name)

@app.route('/add_venture',methods=['GET'])
def add_venture():
	if request.method=='GET':
		name=request.args.get("name")
		loc=request.args.get("loc")
		stt=request.args.get("state")
		dist=request.args.get("dist")
		pin=request.args.get("pin")
		lat=request.args.get("lat")
		lng=request.args.get("lng")
		spec=request.args.get("spec")
		n_beds=request.args.get("n_beds")
		csv_hndl=database.csv_handler()
		stat=csv_hndl.append_csv([loc,name,stt,dist,pin,lat,lng,spec,n_beds])
		#if stat:
		#	flash("Congratulations! a new venture has been added.",'alert alert-success')
		#else: 
		#	flash("Alas! the data already exists",'alert alert-danger')
	#else:
		#flash("Unsupported method of venture management!",'alert alert-danger')

@app.route('/del_venture',methods=['GET'])
def del_venture():
	if request.method=='GET':
		name=request.args.get("name")
		loc=request.args.get("loc")
		stt=request.args.get("state")
		dist=request.args.get("dist")
		pin=request.args.get("pin")
		lat=request.args.get("lat")
		lng=request.args.get("lng")
		spec=request.args.get("spec")
		n_beds=request.args.get("n_beds")
		csv_hndl=database.csv_handler()
		stat=csv_hndl.delete_csv([loc,name,stt,dist,pin,lat,lng,spec,n_beds])
		#if stat:
		#	flash("Congratulations! the venture data has been deleted.",'alert alert-success')
		#else: 
		#	flash("Alas! the data does not exist exists",'alert alert-danger')
	#else:
		#flash("Unsupported method of venture management!",'alert alert-danger')

@app.route('/user_fetch',methods=['GET'])
def user_fetch():
	if request.method=='GET':
		user_data_fetcher=database.user_data()
		res=user_data_fetcher.getUserData()
		response=''
		response+='<br><table border="1px.">'
		response+='<tr style="background-color : blue;">'
		response+='<th>User Id</th>'
		response+='<th>User Name</th>'
		response+='<th>User Mail</th>'
		response+='<th>User Profile picture</th>'
		response+='<th>Action</th>'
		response+='</tr>'
		if len(res)!=0:
			for i in res:
				response+=f"<tr><td>{i[0]}</td><td>{i[1]}</td><td>{i[2]}</td>"
				response+='<td><img src="'+str(i[3])+'" class="profile"></td>'
				if int(i[4])==1:
					response+='<td><input type="submit" class="deactivate" value="Deactivate" onClick="deactivate('+str(i[0])+')"></td></tr>'
				else:
					response+='<td><input type="submit" class="activate" value="Activate" onClick="activate('+str(i[0])+')"></td></tr>'
		return response
			
@app.route('/activate_user',methods=['GET'])
def activate_user():
	if request.method=='GET':	
		uid=request.args.get('userId')
		act_handler=database.activation_handler()
		stat=act_handler.activate(uid)
		#if stat:
		#	flash("Congratulations! the user has been activated.",'alert alert-success')
		#else:
		#	flash("Faced some issue while updaing the status",'alert alert-danger')	
	
@app.route('/deactivate_user',methods=['GET'])
def deactivate_user():
	if request.method=='GET':
		uid=request.args.get('userId')
		act_handler=database.activation_handler()
		stat=act_handler.deactivate(uid)
		#if stat:
		#	flash("Congratulations! the user has been deactivated.",'alert alert-success')
		#else:
		#	flash("Faced some issue while updaing the status",'alert alert-danger')	

@app.route('/intents_fetch',methods=['GET'])
def intents_fetch():
	if request.method=='GET':
		response=''
		with open('intents.json','r') as file:
			data=bot.json.load(file)
		response+='<br><table border="1px."><tr style="background-color : blue;">'
		for i in data['intents']:
			intents=i.keys()
			for j in intents:
				response+=f"<th>{j}</th>"
			response+='</tr>'
			break
		for intents in data['intents']:
			response+='<tr>'
			for header in intents.keys():
				temp=intents[header]
				response+='<td>'
				if type(temp)==type([]):
					for i in temp:
						response+=str(i)+', '
				else:
					response+=str(temp)
					
				response+='</td>'
			response+='</tr>'
		response+='</table>'
		return response


			
@app.route('/change_credit',methods=['GET'])
def change_credit():
	if request.method=='GET':
		val=request.args.get("value")
		mode=request.args.get("mode")
		userId=session['userId']
		if mode=="1":
			# change password.
			registrar=database.Registration()
			registrar.updateProfile(sha256_crypt.encrypt(val),mode,userId)

		elif mode=="2":
			# change username.
			registrar=database.Registration()
			registrar.updateProfile(val,mode,userId)
			
@app.route('/changeProfPic',methods=['POST'])
def changeProfPic():
	if request.method=='POST':
		# change profile pic.
		profilePic=request.files['profpic']	
		fileName=session['profilePic']
		profilePic.save(fileName)
		return redirect(url_for('HomePage'))

@app.route('/vents_fetch',methods=['GET'])
def vents_fetch():
	if request.method=='GET':
		csv_hndl=database.csv_handler()
		res=csv_hndl.getData()
		pattern=request.args.get('pattern')
		temp=[]
		response=''
		response+='<table border="1px.">'
		response+='<tr style="background-color : blue;"><th>Name</th><th>Location</th><th>District</th><th>State</th><th>ZIP code</th></tr>'
		if pattern!='EMPTY':
			for i in res:
				flag=0
				for j in i:
					if str(pattern).lower() in str(j).lower():
						flag=1
						break
				if flag==1:
					temp.append(i)
		else:
			temp=res
		if len(temp)>0:
			for i in temp:
				response+=f"<tr><td>{i[1]}</td><td>{i[0]}</td><td>{i[3]}</td><td>{i[2]}</td><td>{i[4]}</td></tr>"
		response+='</table>'
		return response						
				
'''@app.route('/links_fetch',methods=['GET'])
def links_fetch():
	if request.method=='GET':
		covid_facility=database.State_wise_facility()
		res=covid_facility.get_data()
		temp=[]
		response=''
		response+='<table border="1px.">'
		response+='<tr style="background-color : blue;"><th>Sr No.</th><th>State/UT</th><th>Helpline Number</th><th>State Website link for earmarked COVID facilties</th></tr>'
		temp=res
		if len(temp)>0:
			for i in temp:
				response+=f"<tr><td>{i[0]}</td><td>{i[1]}</td><td>{i[2]}</td><td>{i[3]}</td></tr>"
		response+='</table>'
		return response'''		