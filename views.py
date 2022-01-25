
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import pymysql
db=pymysql.connect(host='localhost',user='root',password='',database='db_veterinary')
c=db.cursor()
# Create your views here.
def index(request):
    return render(request, "index.html")
def login1(request):
    msg = ""
    if (request.POST):
        username = request.POST.get("txtuname")
        password = request.POST.get("txtpasswd")
        s = "select count(*) from tbl_login where txtuname='" + str(username) + "'"
        c.execute(s)
        i = c.fetchone()
        if (i[0] == 0):
            msg = "User doesnt exist"
        else:
            s = "select * from tbl_login where txtuname='" + str(username) + "' and txtpasswd='" + str(password) + "'"
            c.execute(s)
            y = c.fetchone()
            request.session['id'] = y[0]

            if y[3] == 'Admin':
                return HttpResponseRedirect("/showadminhome")

            elif y[3] == 'clinic':
                s = "select * from tbl_staff where email='" + str(username) + "'"

                c.execute(s)
                y = c.fetchone()
                request.session['id'] = y[0]
                return HttpResponseRedirect("/showclinicreg")

    return render(request, "login.html", {"msg": msg})
def login(request):
    return render(request, "login.html")
def showadminhome(request):
	return render(request, "adminform.html")

def showuserreg(request):
    return render(request, "userreg.html")
def showclinicreg(request):
    return render(request, "clinicregistration.html")


"  "














