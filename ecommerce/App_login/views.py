from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import SignUpForm,ProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
# Create your views here.

def signup_user(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Signup Succeefully")
            return HttpResponseRedirect(reverse('App_login:login'))
            #return HttpResponse('Signup successful')
    return render(request,'App_login/signup.html',context={'form':form})
    

def login_user(request):
    form=AuthenticationForm()
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                #return HttpResponse('login successful')
                return HttpResponseRedirect(reverse('App_shop:home'))
    return render(request,'App_login/login.html',context={'form':form})

@login_required
def logout_user(request):
    logout(request)
    messages.warning(request,"Logout Succeefully")
    return HttpResponseRedirect(reverse('App_login:login'))

@login_required
def profile_user(request):
    profile=Profile.objects.get(user=request.user)
    form=ProfileForm(instance=profile)
    if request.method=='POST':
        form=ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Change succeefully saved")
            form=ProfileForm(instance=profile)
    return render(request,'App_login/change_profile.html',context={'form':form})

    
    
