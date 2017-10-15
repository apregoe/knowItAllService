from django.shortcuts import render
from ..models import Review, Topic, UserProfile
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from ..constants import *

def deleteReview(request):
    if request.method != 'POST':
        return JsonResponse(POST_400, status=400, safe=False)

    username = request.GET.get(username_param)
    topicTitle = request.GET.get(topicTitle_param)

    if any(var is None for var in[username, topicTitle]):
        return JsonResponse(deleteReview_400_INVALID_PARAMS, status=400, safe=False)

    try:
        topicID_ = Topic.objects.get(title=topicTitle, category=1)
        userID_ = UserProfile.objects.get(username=username)

    except ObjectDoesNotExist:
        return JsonResponse(DATA_400_NOT_EXISTS(topicTitle + ", or " + username ))

    try:
        Review.objects.get(topicID=topicID_, userID=userID_).delete()

    except ObjectDoesNotExist:
        return JsonResponse({ 'message': username + ' has no review for ' + topicTitle})

    return JsonResponse(deleteReview_SUCESS(username, topicTitle), status=200, safe=False)