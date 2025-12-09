from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout 
from .models import Poll , PollOption , Vote
# Create your views here.
def home(request) :
    polls = Poll.objects.all()
    return render(request , "base/home.html", {"polls":polls})
    
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

def profile(request):
    # it is lock on profile , it only only if user is logged in
    if request.user.is_authenticated :
        return render(request,"base/profile.html")
    return render(request,"base/login.html")

def create_poll(request):
    if request.user.is_authenticated :
    #  using form
        if request.method == "POST" :
            title = request.POST.get('title')
            description = request.POST.get('description')
            category = request.POST.get('category')
            is_public = True if request.POST.get('is_public') else False 
            option = request.POST.getlist('option')
            created_by = request.user
            
            poll = Poll.objects.create(title = title , description = description , 
                                    category = category,
                                    is_public = is_public ,
                                    created_by = created_by 
                                    )
            
            for opt in option :
                polloption = PollOption.objects.create(
                    # option_text = opt,
                    # poll_id = Poll.objects.get(id=poll.poll.id)
                    # FK assignment works using object, not ID.
                    option_text = opt , poll = poll
                                                    )
            messages.success(request,'your poll is created , thank you!!')
            return redirect('home')
        return render(request,'base/create_poll.html')
    return redirect('login')