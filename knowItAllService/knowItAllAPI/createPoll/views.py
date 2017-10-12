from django.http import JsonResponse
from .models import UserProfile, Poll, PollChoice
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from ..constants import *

def createPoll(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400, safe=False)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    username = request.GET.get(username_param)
    text = request.GET.get(text_param)
    choices = request.GET.get(choices_param)
    openForever = request.GET.get(openForever_param)
    dayLimit = request.GET.get(dayLimit_param)

    # Check if all parameters provided
    if any(var is None for var in [username, text, choices, openForever]):
        return JsonResponse(createPoll_400_ALL, status=400, safe=False)

    # Check if openForever is correct
    if not openForever.isdigit():
        return JsonResponse(createPoll_400_OF, status=400, safe=False)
    else:
        openForever = int(openForever)
    if not (0 <= openForever <= 1):
        return JsonResponse(createPoll_400_OF, status=400, safe=False)

    # Check if dayLimit is filled out correctly
    elif openForever == 0 and (dayLimit == None or not dayLimit.isdigit() or int(dayLimit) < 1):
        return JsonResponse(createPoll_400_DL, status=400, safe=False)
    else:
        dayLimit = 0
        openForever = True if openForever==1 else False

    # Store poll into db
    try:
        p = Poll(userID=UserProfile.objects.get(username=username), text=text, numVotes=0, openForever=openForever,
                 dayLimit=dayLimit)
        p.save()
        # Store each choice into db
        cList = choices.split(',')
        for choice in cList:
            c = PollChoice(pollID=p, text=choice)
            c.save()

        return JsonResponse({'status': 200,
                         'message': "Successfully created poll.",
                         'data': {'Poll': p.text, 'choices': cList }}
                        , status=200)
    # Data already exists
    except IntegrityError:
            return JsonResponse(UNIQUE_400, status=400)

    # User does not exist
    except ObjectDoesNotExist:
            return JsonResponse(USER_400, status=400)

