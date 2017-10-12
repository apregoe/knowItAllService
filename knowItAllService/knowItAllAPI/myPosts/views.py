from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db import IntegrityError
from .models import UserProfile, Review, Poll
from ..constants import *
from ..serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView

# Lists all posts of user
class myPosts(APIView):
    # GET request
    def get(self, request):
        username = request.GET.get(username_param)
        try:
            u = UserProfile.objects.get(username=username)
            reviews = Review.objects.filter(userID=u)
            polls = Poll.objects.filter(userID=u)

            reviewsSerializer = ReviewSerializer(reviews, many=True)
            pollsSerializer = PollSerializer(polls, many=True)
            response = reviewsSerializer.data + pollsSerializer.data
            return JsonResponse({'reviews': reviewsSerializer.data, 'polls': pollsSerializer.data }, safe=False)
            # response = reviewsSerializer.data + pollsSerializer.data
            # return JsonResponse({'all': response}, safe=False)

            # Alternative code:
            # reviewsSerializer = ReviewSerializer(reviews, many=True)
            # pollsSerializer = PollSerializer(polls, many=True)
            # response = reviewsSerializer.data + pollsSerializer.data
            # return Response(response)

        # Data already exists
        except IntegrityError:
            return JsonResponse(UNIQUE_400, status=400)

        # User does not exist
        except ObjectDoesNotExist:
            return JsonResponse(USER_400, status=400)

    # POST request
    def post(self, request):
        return JsonResponse(GET_400, status=400)

# https://stackoverflow.com/a/23788795