from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout 
from .models import Poll , PollOption , Vote , comment
from django.db.models import Count
# Create your views here.
def home(request) :
    polls = Poll.objects.all()
    # checking if user voted or not 
    if request.user.is_authenticated :
        voted_polls=[]
        # contains polls id to which user is voted
        # this one make sure that user only get view result option of that poll which he votted 
        # by checking is poll id in voted_polls
        
        
        voted_polls=Vote.objects.filter(user=request.user).values_list('poll_id',flat=True)
        return render(request , "base/home.html", {"polls":polls,'voted_polls':voted_polls})
    else :
        return render(request,"base/home.html",{"polls":polls})
    
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

def voting(request,poll_id,opt_id) :
    #  here we do it to validate if these opt and poll exists in model or user injecting it by itself
    #    like : fake URLs

        # invalid poll IDs

        # invalid option IDs
    poll = Poll.objects.get(id = poll_id)
    option = PollOption.objects.get(id = opt_id)
    # Check if option belongs to poll
    if option.poll != poll:
        messages.error(request, "Invalid option selected.")
        return redirect('home')
    if Vote.objects.filter(user = request.user, poll = poll).exists() :
        messages.error(request,"You have already voted on this poll.")
        return redirect('home')
    # create vote in Vote model
    vote = Vote.objects.create(user=request.user,option=option,poll=poll)
    messages.success(request,"Vote recorded successfully!!")
    return redirect('home')
    
def poll_detail(request,poll_id):
    opt_text = []
    opt_vote = []
    poll = Poll.objects.get(id=poll_id)
    total_votes = Vote.objects.filter(poll=poll_id).count()
    option  = poll.polloption_set.annotate(vote_counts=Count('vote'))
    for opt in option :
        opt_text.append(opt.option_text)
        opt_vote.append(opt.vote_counts)
    
    #  Django ORM → Python lists → JavaScript arrays
    for opt in option:
        if total_votes > 0:
            opt.percentage = round((opt.vote_counts / total_votes) * 100, 2)
            # opt.percentage is field object 
        else:
            opt.percentage = 0
    
    comments = comment.objects.filter(poll = poll).order_by("-commented_on")
    
    # vote = vote_set , set containing vote id to a specific option
    return render(request,'base/poll_detail.html',{'option':option, 
                                                   'poll':poll,
                                                   'opt_text':opt_text,
                                                   'opt_vote':opt_vote,
                                                   'comments':comments,
                                                   
                                                   })
    
def comment_func(request,poll_id):
    if request.method == "POST" and request.user.is_authenticated :
        msg= request.POST.get("message")
        poll = Poll.objects.get(id = poll_id)
        comment.objects.create(user=request.user ,
                               comment_text = msg,
                               poll = poll
                               )
        return redirect("detail", poll_id=poll_id)
    return redirect("detail", poll_id=poll_id)
    
def hide_comment(request,comment_id,poll_id):
    
    message = comment.objects.get(id=comment_id)
    message.delete()
    return redirect("detail", poll_id=poll_id)