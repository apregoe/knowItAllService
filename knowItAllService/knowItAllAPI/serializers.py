from rest_framework import serializers
from .models import *

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review # b/c you import all the classes, need to specify which model
        fields = "__all__" # fields = ('avRating', 'numReviews')

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = "__all__"

# https://stackoverflow.com/a/44979954