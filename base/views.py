from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout 
from .models import Poll , PollOption , Vote , comment
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import PollSerializer , ResultAPISerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request) :
    polls = Poll.objects.annotate(total_vote=Count('vote')).order_by('-created_at')
    hot_poll = polls.first
    # checking if user voted or not 
    if request.user.is_authenticated :
        voted_polls=[]
        # contains polls id to which user is voted
        # this one make sure that user only get view result option of that poll which he votted 
        # by checking is poll id in voted_polls
        
        
        voted_polls=Vote.objects.filter(user=request.user).values_list('poll_id',flat=True)
        return render(request , "base/home.html", {"polls":polls,'voted_polls':voted_polls, "hot_poll":hot_poll})
    else :
        return render(request,"base/home.html",{"polls":polls , "hot_poll":hot_poll})
    
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
            return redirect('signup')
        
        if User.objects.filter(username=username).exists() :
            messages.error(request,"username already exists")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists() :
            messages.error(request,"email already exists")
            return redirect('signup')
            
        #  create user or password hashing (comes with create_user)
        
        user  = User.objects.create_user(username=username , email=email , password=password)
        user.save()
        messages.success(request, "Account created! You can now login.")
        
        return redirect('login')
        
    return render(request,"base/signup.html")

def log_in(request) :
    if request.method == "POST" :
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username = username ).exists():
            # checks if user exists ?
            messages.error(request,"user not found!!")
            return render(request,"base/signup.html")
        
        user = authenticate(request , username=username , password = password)
        # ye output None or not None me dega , check karega ki user database me hai ke nahi
        # ye check karega password correct hai ya nahi 
        if user is None :
            messages.error(request,"password is incorrect!!")
            return redirect('login')
        login(request,user)
        messages.success(request,"logged in successfully!!")
        return redirect("home")
    return render(request, "base/login.html")  
def log_out(request) :
    logout(request)
    messages.success(request,"logged out successfully!!")
    return redirect("home")

@login_required
def dashboard(request):
    # it is lock on profile , it only only if user is logged in
    if request.user.is_authenticated :
        total_polls = Poll.objects.count()
        total_votes = Vote.objects.count()
        total_users = User.objects.count()
        top_poll = Poll.objects.annotate(vote_count=Count('vote')).order_by('-vote').first 
        poll_per_category = Poll.objects.values('category').annotate(total_poll=Count('id'))
        # it says : poll.vote_count
        return render(request,"base/dashboard.html",{'total_polls':total_polls,
                                                     'total_votes':total_votes,'total_users':total_users,
                                                     'top_poll':top_poll,
                                                     'category_wise':poll_per_category})
    return redirect('login')

@login_required
def medashboard(request):
    
        total_polls = Poll.objects.filter(created_by=request.user).count()
        polls  = Poll.objects.filter(created_by=request.user).annotate(total_vote=Count('vote'))
        voted_polls_count = Vote.objects.filter(user=request.user).count()
        voted_polls=Vote.objects.filter(user=request.user).values_list('poll_id',flat=True)
        all_polls_id=Poll.objects.values_list('id',flat=True)
        all_polls=Poll.objects.all()
        return render(request,'base/medashboard.html',{'total_polls':total_polls,
                                                       'polls':polls,
                                                       "voted_polls" : voted_polls,
                                                       "voted_polls_count":voted_polls_count,
                                                       "all_polls_id":all_polls_id,
                                                       "all_polls" : all_polls
                                                       })
        
@login_required
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

@login_required
def voting(request,poll_id,opt_id) :
    #  here we do it to validate if these opt and poll exists in model or user injecting it by itself
    #    like : fake URLs

        # invalid poll IDs

        # invalid option IDs
    poll = get_object_or_404(Poll, id=poll_id)
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
    
@login_required
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
                                                   'total_votes':total_votes
                                                   })
 
@login_required   
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
 
@login_required   
def hide_comment(request,comment_id,poll_id):
    
    message = comment.objects.get(id=comment_id)
    message.delete()
    return redirect("detail", poll_id=poll_id)

@login_required
def edit_comment(request, comment_id, poll_id):
    if request.method == 'POST':
        text = request.POST.get("message")

        comment_obj = get_object_or_404(comment, id=comment_id)

        comment_obj.comment_text = text
        comment_obj.save()

        return redirect("detail", poll_id=poll_id)

    return redirect("detail", poll_id=poll_id)


@login_required
def undo_vote(request,poll_id):
    poll = Poll.objects.get(id=poll_id)
    vote = Vote.objects.get(poll=poll,user = request.user)
    vote.delete()
    return redirect('home')
    
@login_required
def delete_poll(request,poll_id):
    poll = Poll.objects.get(id=poll_id)
    poll.delete()
    return redirect('home')
    
class PollListAPIView(APIView) :
    # We use many=True because the queryset contains multiple objects and 
    # the serializer needs to return a list of JSON objects.
    def get(self,request):
        polls = Poll.objects.all()
        serializer = PollSerializer(polls,many=True)
        return Response(serializer.data)
    
class PollDetailAPIView(APIView):
    def get(self,request,poll_id):
        poll = Poll.objects.get(id=poll_id)
        serializer = PollSerializer(poll)
        return Response(serializer.data)
    
class ResultAPIView(APIView) :
    def get(self,request,poll_id):
        poll = Poll.objects.get(id=poll_id)
        total_votes = Vote.objects.filter(poll=poll).count()
        result = []
        for options in poll.polloption_set.all() :
            per_vote = Vote.objects.filter(poll=poll,option=options).count() 
            percentage = ((per_vote*100)/total_votes
                          if total_votes > 0 
                          else 0
                          )
            result.append({
                "option": options.option_text,
                "vote" : per_vote,
                "percentage" : round(percentage,2)
            })
            
        serializer = ResultAPISerializer(result,many=True)
        return Response(
            {
            "poll": {
                "id": poll.id,
                "title": poll.title
            },
            "total_votes": total_votes,
            "results": serializer.data
        }
        )
            
        
        