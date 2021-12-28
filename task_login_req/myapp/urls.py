from django.urls import path
from .import views
urlpatterns = [
    path('home/',views.home),
    path('login/',views.loginhandle),
    path('createdetails/',views.createdetails),
    path('logout/',views.logouthandle),
    path('dashboard/',views.dashboard),
]
