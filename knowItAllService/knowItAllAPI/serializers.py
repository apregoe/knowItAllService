from rest_framework import serializers
from .models import *

class PollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        # fields = ('avRating', 'numReviews')
        fields = "__all__"