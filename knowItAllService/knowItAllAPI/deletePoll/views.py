from ..models import Poll
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from ..constants import *

#/api/
def deletePoll(request):

    if request.method != 'POST':
        return JsonResponse(POST_400, status=400, safe=False)

    username = request.GET.get(username_param)
    pollText = request.GET.get(pollText_param)

    if any(var is None for var in [username, pollText]):
        return JsonResponse(deletePoll_400_ALL, status=400, safe=False)

    try:
        poll = Poll.objects.filter(text=pollText)
        if poll.exists():
            poll = Poll.objects.get(text=pollText).delete()
            deletePoll_200_SUCCESS['pollDeleted'] = pollText
            return JsonResponse(deletePoll_200_SUCCESS, status=400, safe=False)
        else:
            return JsonResponse(deletePoll_400_UNSUCCESSFUL, status=400, safe=False)

    except ObjectDoesNotExist:
        JsonResponse(DATA_400, status=400, safe=False)