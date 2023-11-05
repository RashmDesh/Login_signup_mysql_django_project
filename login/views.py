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

def generateOTP() :
    digits = "0123456789"
    create_OTP = ""

    for i in range(6) :
       create_OTP += digits[math.floor(random.random() * 10)]
 
    return create_OTP


# Create your views here.
def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            Registeruser.objects.get(email=email)
        except:
             return HttpResponse("User does not exists. ")
            
        else:
            obj=Registeruser.objects.get(email=email)
            name=obj.name
            getpass=obj.password

            decode_pass=pbkdf2_sha256.verify(password,getpass)

            if obj.email==email and decode_pass == True:
                    context= {'data':name}
                    return render(request,"result.html",context)
            else:
                    return HttpResponse("Please check password")


        '''
        if Registeruser.objects.get(email=email):
                obj=Registeruser.objects.get(email=email)
                name=obj.name
                getpass=obj.password

                decode_pass=pbkdf2_sha256.verify(password,getpass)

                if obj.email==email and decode_pass == True:
                    context= {'data':name}
                    return render(request,"result.html",context)
                else:
                    return HttpResponse("Please check password")
                
        else:
            return HttpResponse("Please check usernam ")
       
       '''
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

        '''
        try:
            obj=Registeruser.objects.get(email=email)
        except:
             return HttpResponse("User does not exists. ")
            
        else: 
        '''
        obj=Registeruser.objects.get(email=email)
        obj.password=newpass_encode
        obj.save()

        global OTP
        OTP=generateOTP()
        subject = 'OTP for password change'
        message = f'Hi,{obj.name} \n OPT is :{OTP}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list )
        return redirect("/login/otp/")

    return render(request,"updatepassword.html")

def otp(request):
    if request.method == "POST":
        otp=request.POST.get('otp')
        global OTP
        if OTP == otp:
            return redirect("/login/otpresult/")
        else:
            return HttpResponse("Incorrect OTP")
    
    if request.method=="GET":
         return render(request,"otp.html")
    

def optresult(request):
     return render(request,"otp_result.html")