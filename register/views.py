from django.shortcuts import render
from .models import Registeruser
from  passlib.hash import pbkdf2_sha256
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
def register(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')

        enc_pass = pbkdf2_sha256.hash(password)

        ''' 
        user_data=Registeruser(name=name,email=email,phone=phone,password=enc_pass)
        user_data.save()
        context={'data':name}
        return render(request,"register_result.html",context)
        
        ''' 
      
        try:
            Registeruser.objects.get(email=email)
            
        except:
            user_data=Registeruser(name=name,email=email,phone=phone,password=enc_pass)
            user_data.save()
            context={'data':name}

            subject = 'welcome to RD channel'
            message = f'Hi {name}, thank you for registering with us'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list )

            return render(request,"register_result.html",context)
        else:
            context={'data':"User already register"}
            return render(request,"register_result.html",context)

    return render(request,"register.html")