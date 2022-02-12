import mailbox
import db
from flask import Flask,render_template,request,session,redirect
import mysql.connector
import json
from werkzeug.utils import secure_filename
import os
import difflib 
app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'petsake123@gmail.com'
app.config['MAIL_PASSWORD'] = 'Pet@123456789'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.secret_key="admin"
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 


@app.route("/")
def main():

	return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
	username=request.form.get('txtuname')
	password=request.form.get('txtpasswd')
	r=db.dblogsel(username,password)
	
	print(r)
	if r==False:
		return render_template("message.html",message="Invalid username or password",route="/login1")
	elif r[0][0] == "clinic":
		status=db.getclinicstatus(username)
		if(status == 'Requested'):
			return render_template("message.html",message="your account is not verified yet",route="/login1")
		elif(status == 'Reject'):
			return render_template("message.html",message="sorry,your account is rejected",route="/login1")
		else:
			session['useremail']=username
			session['usertype']=r[0][0]
			return redirect("showclinichome")
	elif r[0][0] == "doctor":
		session['useremail']=username
		session['usertype']=r[0][0]
		return redirect("doctorhome")
	elif r[0][0] == "admin":
		session['useremail']=username
		session['usertype']=r[0][0]
		return redirect("showadminhome")
@app.route("/login1")
def login1():
	return render_template("login.html")	
@app.route("/showadminhome")
def showadminhome():
	return render_template("admin/adminform.html")	
@app.route("/doctorhome")
def doctorhome():
	return render_template("doctor/home.html")	
@app.route("/saveclinicreg",methods=['GET','POST'])	

@app.route("/saveclinicreg",methods=['GET','POST'])	
def saveclinicreg():
	file = request.files['file']
	if file:
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		print(filename)
	name=request.form.get('txtclname')
	reg=request.form.get('txtclregnum')
	place=request.form.get('place')
	district=request.form.get('district')
	state=request.form.get('state')
	phone=request.form.get('txtclphn')
	pincode=request.form.get('txtpin')
	email=request.form.get('txtclemail')
	govform=request.form.get('govform')
	txtname=request.form.get('txtname')
	address=request.form.get('address')
	txtphn=request.form.get('txtphn')
	password=request.form['txtpswrd']
	ques=request.form['txtquestion']
	ans=request.form['txtans']
	db.saveclinic(name,reg,place,district,state,phone,pincode,email,govform,txtname,address,txtphn,password,ques,ans,filename)
	return render_template("message.html",message="Registration Successfull",route="/login1")	

@app.route("/showclinicreg")
def showclinicreg():
	state=db.dbstate()
	return render_template("clinicregistration.html",state=state)	

@app.route("/showclinichome")
def showclinichome():
	return render_template("clinic/home.html")	
@app.route("/savespecies",methods=['GET','POST'])	
def savespecies():
	name=request.form['sname']
	pdisease=request.form['distopet']
	hdisease=request.form['disfrompet']
	food=request.form['food']
	symptoms=request.form['symptoms']
	medicine=request.form['vacmed']
	db.savesp(name,pdisease,hdisease,food,symptoms,medicine)
	return render_template("message.html",message="Saved Successfull",route="/showadminhome")
@app.route("/showspecies")
def showspecies():
	return render_template("admin/species.html")

@app.route("/savebreed",methods=['GET','POST'])	
def savebreed():
	name=request.form['species']
	breed=request.form['breed']
	pdisease=request.form['distopet']
	hdisease=request.form['disfrompet']
	food=request.form['food']
	symptoms=request.form['symptoms']
	medicine=request.form['vacmed']
	db.savebr(name,breed,pdisease,hdisease,food,symptoms,medicine)
	return render_template("message.html",message="Added Successfully",route="/showadminhome")

@app.route("/showbreed")
def showbreed():
	species=db.dbspecies()
	return render_template("admin/breed.html",species=species)	
@app.route("/getBreed",methods=['GET','POST'])
def getBreed():
	selectedBreed=request.form.get("selectedBreed")
	species=request.form["species"]
	if selectedBreed == None : 
		breed=db.dbbreed(species)
		s="""<div class=form-group>
            <label for=sel1>Breed</label>

          <select required name=breed class=form-control><option selected>------SELECT-----</option>"""
		for b in breed:
			s=s+"<option value=" + str(b[1]) +">"+b[2]+"</option>"
		s=s+"</select></div>"
		return s
	else:
		breed=db.dbbreed(species)
		s="""<div class=form-group>
            <label for=sel1>Breed</label>

          <select required name=breed class=form-control><option selected>------SELECT-----</option>"""
		for b in breed:
			if str(selectedBreed) == str(b[1]):
				s=s+"<option  selected value=" + str(b[1]) +">"+b[2]+"</option>"
			else:
				s=s+"<option   value=" + str(b[1]) +">"+b[2]+"</option>"
		s=s+"</select></div>"
		return s
@app.route("/savevacc",methods=['GET','POST'])	
def savevacc():
	sname=request.form['species']
	age=request.form['txtage']
	weekmonth=request.form['txtweekmonth']
	vacc=request.form['vacc']
	desc=request.form['desc']
	db.savevacc(sname,age,weekmonth,vacc,desc)
	return render_template("message.html",message="Added Successfully",route="/showadminhome")

@app.route("/showvaccination")
def showvaccination():
	species=db.dbspecies()
	return render_template("admin/vaccination.html",species=species)	




if __name__ == '__main__':
    app.run(debug=True)