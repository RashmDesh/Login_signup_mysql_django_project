from django.shortcuts import render,redirect
from .models import Registeruser
from  passlib.hash import pbkdf2_sha256
from django.conf import settings
from django.core.mail import send_mail
from login.views import generateOTP,validate_password


# Create your views here.
def register(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')

        enc_pass = pbkdf2_sha256.hash(password)

        try:
            Registeruser.objects.get(email=email)
            
        except:
            if validate_password(password):
              
                OTP=generateOTP()

                request.session['otp']=OTP
                request.session['name']=name
                request.session['email']=email
                request.session['phone']=phone
                request.session['password']=enc_pass


                subject = 'OTP form blogger'
                message = f' OPT is :{OTP}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail( subject, message, email_from, recipient_list )
                return redirect("/registerotp/")
                #return render(request,"register_result.html",context)
            else:
                msg="Invalid password. Please follow password condition"
                render(request,"register.html",{'msg':msg})

           
        else:
            context={'data':"User already register"}
            return render(request,"register_result.html",context)

    return render(request,"register.html")

def registerotp(request):
    if request.method == "POST":
        otp=request.POST.get('otp')
        otp_session=request.session["otp"]
        if otp == otp_session:   
            name=request.session['name']
            email=request.session['email']
            phone=request.session['phone']
            enc_pass=request.session['password']

            user_data=Registeruser(name=name,email=email,phone=phone,password=enc_pass)
            user_data.save()
            context={'data':name}
            return render(request,"register_result.html",context)
        else:
            msg="Incorrect OTP"
            return render(request,"register.html",{"msg":msg})
    
    if request.method=="GET":
        return render(request,"otp.html")