from django.shortcuts import render,redirect
from  passlib.hash import pbkdf2_sha256
from  register.models import Registeruser
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
import math, random
import logging
logger = logging.getLogger(__name__)


OTP=""
email=""
newpass_encode=""

def generateOTP() :
    digits = "0123456789"
    create_OTP = ""

    for i in range(6) :
       create_OTP += digits[math.floor(random.random() * 10)]
 
    return create_OTP

def validate_password(password: str):
    if len(password)>=8:
        lower = 0
        upper = 0
        special = 0
        number = 0
        for i in password:
            if i.islower():
                lower += 1
            
            elif i.isupper():
                upper += 1

            elif i.isnumeric():
                number += 1

            elif i in "~!@#$%^&*()_[]()":
                special += 1

        if lower>=1 and upper>=1 and number>=1 and special>=1:
                return True
    return False


# Create your views here.
def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            Registeruser.objects.get(email=email)
        except:
            msg="User does not exiat"
            return render(request,"login.html",{"msg":msg})
            
        else:
            obj=Registeruser.objects.get(email=email)
            name=obj.name
            getpass=obj.password

            decode_pass=pbkdf2_sha256.verify(password,getpass)

            if obj.email==email and decode_pass == True:
                    request.session["email"]=email
                   # request.session["islogin"]="true"
                    context= {'data':name}
                    return render(request,"result.html",context)
            else:
                    msg="Invalid password"
                    return render(request,"login.html",{"msg":msg})
    return render(request,"login.html")

'''
def result(request):
    data= request.POST.get('email')
    context= {'data':data}
    return render(request,"result.html",context)
'''

def update(request):
    if request.method=='POST':
        email=request.POST.get('email')
        oldpassword=request.POST.get('oldpassword')
        newpassword=request.POST.get('newpassword')

        
        newpass_encode= pbkdf2_sha256.hash(newpassword)
        request.session['email']=email
        request.session['newpassword']=newpass_encode

        try:
            Registeruser.objects.get(email=email)
        except:
             return HttpResponse("User does not exists. ")
            
        else: 
            obj=Registeruser.objects.get(email=email)

            OTP=generateOTP()
            request.session['otp']=OTP
            subject = 'OTP for password change'
            message = f'Hi,{obj.name} \n OPT is :{OTP}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list )
           
            return redirect("/login/otp/")
           # return render(request,"otp.html")

    return render(request,"updatepassword.html")

def otp(request):
    if request.method == "POST":
        otp=request.POST.get('otp')
        otp_session=request.session["otp"]
        email=request.session["email"]
        if otp==otp_session:
            obj=Registeruser.objects.get(email=email)
            newpass_encode=request.session['newpassword']
            obj.password=newpass_encode
            obj.save()
            return  render(request,"otp_result.html")
        else:
            msg="Incorrect OTP"
            return render(request,"otp.html",{"msg":msg})
    
    if request.method=="GET":
        return render(request,"otp.html")
    

def logout(request):
    try:
        del request.session['email']
    except:
        return redirect('/login/')
    return redirect('/login/')
