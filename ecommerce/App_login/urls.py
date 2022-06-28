from django import views
from django.urls import include, path
from . import views

app_name='App_login'

urlpatterns = [
    path('signup/',views.signup_user,name='signup'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('profile/',views.profile_user,name='profile')
]
