from django.shortcuts import render
from  passlib.hash import pbkdf2_sha256
from  register.models import Registeruser
from django.http import HttpResponse

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
    return render(request,"updatepassword.html")