from django.conf.urls import url
from django.urls import path,include
from . import views
urlpatterns = [
    path('home/',views.home),
    url(r'^signup/$', views.signup, name='signup'),
    path(
    'activate/<slug:uidb64>/<slug:token>/',
    views.activate, 
    name='activate'),
    path('loginhandle/', views.loginhandle, name = "loginhandle"),
    path('logouthandle/', views.logouthandle, name = "logouthandle"),

]