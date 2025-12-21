from rest_framework import serializers
from .models import Poll , PollOption , Vote
# “I used a ModelSerializer to control how Poll objects are exposed via JSON, and 
# I customized related fields like created_by to expose only safe, meaningful data.”

# defining polloption serializer

class PollOptionSerializer(serializers.ModelSerializer) :
    class Meta :
        model = PollOption
        fields=[
            "id",
            "option_text",
        ]
        
class ResultAPISerializer(serializers.Serializer):
        # here we describe the structure of json 
        option = serializers.CharField()
        vote = serializers.IntegerField()
        percentage = serializers.FloatField()
        
class PollSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source="created_by.username")
# initially created_by contains raw id which has no use for the client but .username has text which is useful
    options = PollOptionSerializer(
        source = "polloption_set",
        many =True,
        read_only = True
    )
    class Meta:
        model = Poll
        fields = [
            "id",
            "title",
            "description",
            "category",
            "created_at",
            "created_by",
            "options"
        ]
# these fields are exposed to the browser or client 

