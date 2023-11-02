from django.shortcuts import render
from .models import Registeruser
from  passlib.hash import pbkdf2_sha256


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
            context={'data':"Email already exisis"}
            return render(request,"register_result.html",context)
        else:
            user_data=Registeruser(name=name,email=email,phone=phone,password=enc_pass)
            user_data.save()
            context={'data':name}
            return render(request,"register_result.html",context)
          
        
        
    
    return render(request,"register.html")