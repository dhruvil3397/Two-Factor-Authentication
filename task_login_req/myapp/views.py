from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Student
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
    return render(request,'base.html')

def loginhandle(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request=request,data = request.POST )
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname , password =upass)
            if user is not None:
                login(request,user)
                param = "create"
                return render(request,'base.html',{'param':param})
    fm = AuthenticationForm()
    return render(request,'login.html',{'form':fm})

@login_required(login_url='/home/')
def createdetails(request):
    if request.method =='POST':
        name = request.POST.get('name')
        roll = request.POST.get('roll')
        city = request.POST.get('city')
        print(name)
        stu = Student(name =name,roll=roll,city=city)
        stu.save()
        param = "create"
        return render(request,'base.html',{'param':param})
    param = "create"
    return render(request,'base.html',{'param':param})

@login_required(login_url='/home/')
def dashboard(request):
    stu = Student.objects.all()
    return render(request,'dashboard.html',{'student':stu})

def editdeatails(request):
    id = request.GET.get("id")
    print(id)
    


def logouthandle(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/home/')
    return HttpResponse('404')