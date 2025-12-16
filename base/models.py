from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Poll(models.Model) :
    title = models.CharField(max_length=20)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=10)
    is_public = models.BooleanField(default=True)
    
class PollOption(models.Model) :
    option_text = models.TextField(max_length=100)
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE)
    
class Vote(models.Model):
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class comment(models.Model) :
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=100)
    commented_on = models.DateTimeField(auto_now_add=True)
    
    
    
    