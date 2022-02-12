import pymysql
import datetime
from datetime import timedelta
db=pymysql.connect(host="localhost",user="root",password="",db="db_vet")
def dblogsel(username,password):
	sql = "select usertype from tbl_login where username='"+username+"' and password='"+password+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	if len(result)==1:
		return list(result)
	else:
		return False
def saveclinic(name,reg,place,district,state,phone,pincode,email,govform,txtname,address,txtphn,password,ques,ans,filename):
	sql1="""insert into tbl_clinicreg(clinic_name,clinic_reg_no,state,district,place,pincode,phone,clinic_email_id,govt_no,form,name,address,phno) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
	val1=(name,reg,state,district,place,pincode,phone,email,govform,filename,txtname,address,txtphn)
	cursor=db.cursor()
	cursor.execute(sql1,val1)
	sql = """INSERT INTO tbl_login(email,password,usertype,securityque,securityans) VALUES ( %s,%s,%s, %s,%s)"""
	val = (email,password,'clinic',ques,ans) 
	cursor=db.cursor()
	cursor.execute(sql,val)
	db.commit()
	return True
def getclinicstatus(email):
	sql="select c.status from tbl_clinicreg c where c.clinic_email_id='"+email+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchone()
	return(result[0])
def dbstate():
	sql="select * from tbl_state"
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	return(result)

def dbdistrict(state):
	sql="select * from tbl_district where stateid='"+ str(state) +"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	return(result)
	print(list(result))
	return result
def dbclinic(email):
	sql="select c.clinic_email_id,c.clinic_name from tbl_clinicreg c,tbl_userreg u where u.pincode=c.pincode and u.place=c.place and u.email='"+str(email)+"'"
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	return(result)
def savesp(name,pdisease,hdisease,food,symptoms,medicine):
	sql1="""insert into tbl_species(spname,pdisease,hdisease,food,symptoms,medicine) VALUES (%s,%s,%s,%s,%s,%s)"""
	val1=(name,pdisease,hdisease,food,symptoms,medicine)
	cursor=db.cursor()
	cursor.execute(sql1,val1)
	db.commit()
	return True
def savebr(name,breed,pdisease,hdisease,food,symptoms,medicine):
	sql1="""insert into tbl_breed(spid,breedname,pdisease,hdisease,food,symptoms,medicine) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
	val1=(name,breed,pdisease,hdisease,food,symptoms,medicine)
	cursor=db.cursor()
	cursor.execute(sql1,val1)
	db.commit()
	return True
def dbspecies():
	sql="select * from tbl_species"
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	return(result)
	
def dbbreed(species):
	sql="select * from tbl_breed where spid='"+ str(species) +"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	return(result)
	print(list(result))
	return result
def getvaccdetails(email):
	sql="select u.name,u.age,u.weekmonth,u.dateofreg from tbl_userpetdetails u WHERE u.email='"+email+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	res=list(result) 
	print(res)
	v=[]
	for r in res:
		var=r[3]
		a=datetime.datetime.strptime(var, '%Y-%m-%d')
		d=""
		if(r[2] == "weeks"):
			d = a - timedelta(days=(r[1]*7))
		elif(r[2] == "months"):
			d = a - timedelta(days=(r[1]*30))
		# print(d)
		b=datetime.datetime.today()-d
		# print(b)
		# print(abs(b.days))
		sql1="select u.pname,s.spname,v.age,v.weekmonth,v.vacc,v.description from tbl_vacc v,tbl_userpetdetails u,tbl_species s where u.name=s.spid and u.email='"+email+"' and v.sname='"+str(r[0])+"' and v.sname= u.name "
		print(sql1)
		c=abs(b.days)
		cursor=db.cursor()
		cursor.execute(sql1)
		result=cursor.fetchall()
		# print(result)
		data=list(result)
		for d in data:
			age=""
			if(d[3] == "weeks"):
				age=int(d[2])*7
			elif(d[3] == "months"):
				age=int(d[2])*30
			# print(age)
			if(age-c <= 14 and age-c >= 0):
				v.append(d)
	return v	
				





