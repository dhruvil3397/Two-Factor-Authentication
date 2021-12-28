from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate,logout
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

def home(request):
    return render(request,'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            print(current_site)
            mail_subject = 'Activate your blog account.'
            # Render the message into html:-------
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            print(account_activation_token.make_token(user),'-------------')
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# For activation:-----------
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
       
        # return redirect('home')
        msg = 'Thank you for your email confirmation. Now you can login your account.'
        return render(request,'home.html',{'msg':msg})
    else:
        return HttpResponse('Activation link is invalid!')


def loginhandle(request):
    if request.method == "POST":
        loginusername = request.POST.get('username')
        loginpassword = request.POST.get('password')
        print(loginusername)
        print(loginpassword)
        a = User.objects.filter(username=loginusername)
        print(len(a))
        if len(a) != 0:
            u = User.objects.get(username=loginusername)
            print(u)
            print(u.is_active)
            if u.is_active ==True:
                user = authenticate(username=loginusername, password=loginpassword)
                if user is not None:
                    print("+++++++++++++++++++++++")
                    print(user)
                    login(request, user)
                    param = "Welcome to the Dashboard"
                    return render(request, 'home.html', {'param': param})
        
                return HttpResponse('User not found')
            return HttpResponse('Please verify the email link')
        return HttpResponse('User not found')
    return HttpResponse('404 - Not Found')

def logouthandle(request):
    if request.user.is_authenticated:
        logout(request)
        data = "You have successfully logout"
        return render(request,'home.html',{'data':data})
    return HttpResponse('404 - Not Found')


