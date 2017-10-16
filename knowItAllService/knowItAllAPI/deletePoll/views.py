from ..models import Poll, UserProfile
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from ..constants import *
from django.views.decorators.csrf import csrf_exempt

#ex call:
@csrf_exempt
def deletePoll(request):

    if request.method != 'POST':
        return JsonResponse(POST_400, status=400, safe=False)

    username = request.GET.get(username_param)
    pollText = request.GET.get(pollText_param)

    if any(var is None for var in [username, pollText]):
        return JsonResponse(deletePoll_400_ALL, status=400, safe=False)

    try:

        userID = UserProfile.objects.get(username=username)
        pollID = Poll.objects.get(text=pollText)

        if pollID.userID != userID:
            return JsonResponse(deletePoll_USERNAMEISNOTOWNER(username, pollText))
        else:
            pollID.delete()
            return JsonResponse(deletePoll_200_SUCCESS, status=400, safe=False)

    except ObjectDoesNotExist:
        return JsonResponse(DATA_400_NOT_EXISTS(pollText + ' or ' + username), status=400, safe=False)