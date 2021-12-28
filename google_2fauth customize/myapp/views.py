from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import match_token,login as otp_login
from django_otp import devices_for_user
import pyotp  
import base64
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
    return render(request,'myapp/base.html')

# For new user's registration :-------------------
def registration(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(username)
        print(email)
        print(password)
        user = User.objects.create_user(username,email,password)
        user.save()
        user = authenticate(username = username,password = password)
        print(user)
        if user is not None :
            login(request,user)
            return render(request,'myapp/enable.html')
        return HttpResponse('Invalid User')
    return render(request,'myapp/registration.html')


# secret key generation for particular users :-------------
class generateKey:
    @staticmethod
    def returnValue(email):
        return 'JBSWY3DPEHPK3PXP'+str(email)

# QR code generation and render into html page:------------
def qr(request):
    user = request.user
    print(user)
    if user is request.user:
        u = User.objects.get(username=user)
        print(u)
        email = u.email

        keygen = generateKey()             
        key = base64.b32encode(keygen.returnValue(email).encode())
        print(key)       
        totp = pyotp.TOTP(key)
        otp = totp.now()
        print(otp)

        auth_str = totp.provisioning_uri(name=str(user),issuer_name=str(user))
        print(auth_str)

        #SVG stands for Scalable Vector Graphics.
        #SVG defines vector-based graphics in XML format.
        context = {}
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(auth_str, image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)
        context["svg"] = stream.getvalue().decode() 
    
        return render(request,'myapp/qrcode.html',context=context)
    return HttpResponse('Invalid User')

def user_otp(request):
    if request.method =='POST':
        user = request.user
        print(user)
        u = User.objects.get(username=user)
        print(u)
        email = u.email
        keygen = generateKey()         
        key = base64.b32encode(keygen.returnValue(email).encode())
        print(key)
       
        otp_token = request.POST.get('token')
        print(otp_token)
        totp = pyotp.TOTP(key)
        verify = totp.verify(otp_token)
        print(verify)
        if verify == True:
            cnf = TOTPDevice.objects.get_or_create(user=user)
            my = TOTPDevice.objects.get(user=user)
            my.name = str(user)
            print(my.name)
            my.save()
            print(my.confirmed)
            if my.confirmed == False:
                my.confirmed = True
                my.save()
            
            print('*******')
            return render(request,'myapp/success.html')
        return HttpResponse('Verification Failed')
    return HttpResponse('Sorry')
         

def loginhandle(request):
    if request.method  == "POST" :
        loginusername = request.POST.get('username','default')     
        loginpassword = request.POST.get('password','default')
        user = authenticate(username = loginusername,password = loginpassword)
        print(user)
        if user is not None :
            login(request,user)
            # This TOTPDevice gives user's device data,to check whether is confirmed to use 2FA or not
            cnf = TOTPDevice.objects.get(user=user)
            print(cnf.confirmed)
            print('*******')
            if cnf.confirmed ==True:
                return render(request,'myapp/loginotp.html')
            else :
                msg = "Your 2 FA is disable"
                return render(request,'myapp/base.html',{'msg':msg})


        return HttpResponse('User not found')
   
    return HttpResponse('404 - Not Found')

def loginotp(request):
    if request.method == 'POST':
        user = request.user
        print(user)
        if user is request.user:
            u = User.objects.get(username=user)
            print(u)
            email = u.email
            # user = User.objects.get()
            keygen = generateKey()
                            
            key = base64.b32encode(keygen.returnValue(email).encode())
            print(key)
            
            totp = pyotp.TOTP(key)
            otp = totp.now()
            print(otp)
            auth_str = totp.provisioning_uri(name=str(user),issuer_name=str(user))
            print(auth_str)
            context = {}
            factory = qrcode.image.svg.SvgImage
            img = qrcode.make(auth_str, image_factory=factory, box_size=20)
            stream = BytesIO()
            img.save(stream)
            context["svg"] = stream.getvalue().decode() 
            return render(request,'myapp/qrcode.html',context=context)
    return HttpResponse('Invalid User')


def logouthandle(request):
    logout(request)
    print('logout')
    return redirect('/myapp/home/')
    
def verifyotp(request):
    if request.method =='POST':
        user = request.user
        print(user)
        u = User.objects.get(username=user)
        print(u)
        email = u.email
        keygen = generateKey()         
        key = base64.b32encode(keygen.returnValue(email).encode())
        print(key)
       
        otp_token = request.POST.get('token')
        print(otp_token)
        totp = pyotp.TOTP(key)
        verify = totp.verify(otp_token)
        print(verify)
        param = "Your 2 FA is Enable"
        return render(request,'myapp/base.html',{'param':param})
    return HttpResponse('404 - Not Found')

def disable2fa(request):
    try :
        user = request.user
        my = TOTPDevice.objects.get(user=user)
        my.confirmed = False
        my.save()
        msg = "Your 2FA is Disable"
        return render(request,'myapp/base.html',{'msg':msg})
    except:
        return HttpResponse('404-Not Found')
