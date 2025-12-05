from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout 
# Create your views here.
def home(request) :
    return render(request , "base/home.html")
    
def sign_up(request):
    # info collection
    if request.method == 'POST' :
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
    
    # info validation
    
        if cpassword!=password :
            messages.error(request,"password does not match, try again")
            return render(request,"base/signup.html")
        
        if User.objects.filter(username=username).exists() :
            messages.error(request,"username already exists")
            return render(request,"base/signup.html")
        
        if User.objects.filter(email=email).exists() :
            messages.error(request,"email already exists")
            return render(request,"base/signup.html")
            
        #  create user or password hashing (comes with create_user)
        
        user  = User.objects.create_user(username=username , email=email , password=password)
        user.save()
        messages.success(request, "Account created! You can now login.")
        logout(request)
        return render(request,"base/home.html")
        
    return render(request,"base/signup.html")

def log_in(request) :
    if request.method == "POST" :
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request , username=username , password = password)
        # ye output None or not None me dega
        if user is not None :
            login(request,user)
            messages.success(request,"logged in successfully!!")
            return redirect("home")
        else :
            messages.error(request,"user not found!!")
            return render(request,"base/signup.html")
    else :
        return render(request,"base/login.html")
            
def log_out(request) :
    logout(request)
    messages.success(request,"logged out successfully!!")
    return redirect("home")