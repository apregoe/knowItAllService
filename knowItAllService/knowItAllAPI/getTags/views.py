from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db import IntegrityError
from .models import *
from ..constants import *
from ..serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView

# Get specific poll or topic
class getPost(APIView):
    # GET request
    def get(self, request):
        type = request.GET.get(type_param)
        text = request.GET.get(text_param)
        
        try:
            if type == 'topic':
                topic = Topic.objects.filter(title=text)
                topicSerializer = TopicSerializer(topic, many=True)
                reviews = Review.objects.filter(topicID=topic)
                reviewsSerializer = ReviewSerializer(reviews, many=True)
                return JsonResponse({'status': 200, 'topic': topicSerializer.data, 'reviews': reviewsSerializer.data }, safe=False)

            elif type == 'poll':
                poll = Poll.objects.filter(text=text)
                pollSerializer = PollSerializer(poll, many=True)
                pc = PollChoice.objects.filter(pollID=poll)
                pcSerializer = PollChoiceSerializer(pc, many=True)
                return JsonResponse({'status': 200, 'poll': pollSerializer.data, 'pc': pcSerializer.data }, safe=False)

            # Type is incorrect
            else:
                return JsonResponse(getPost_400_TP, status=400)

        # Data does not exist
        except ObjectDoesNotExist:
            return JsonResponse(DATA_400, status=400)

    # POST request
    def post(self, request):
        return JsonResponse(GET_400, status=400)

# https://stackoverflow.com/a/23788795