from django.urls import path,include
from .import views

urlpatterns = [
    path('home/',views.home),
    path('registration/',views.registration),
    path('qrcode/',views.qr),
    path('user_otp/',views.user_otp),
    path('loginhandle/', views.loginhandle, name = "loginhandle"),
    path('logouthandle/', views.logouthandle, name = "logouthandle"),
    path('loginotp/',views.loginotp),
    path('verifyotp/',views.verifyotp),
    path('disable2fa/',views.disable2fa),
]
