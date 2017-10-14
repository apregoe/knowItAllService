from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from ..models import *
from django.db import IntegrityError
from ..constants import *
from decimal import Decimal

def vote(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400, safe=False)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    username = request.GET.get(username_param)
    pollText = request.GET.get(pollText_param)
    pollChoiceText = request.GET.get(pollChoiceText_param)

    # Check if all parameters provided
    if any(var is None for var in [username, pollText, pollChoiceText]):
        return JsonResponse(vote_400_ALL, status=400, safe=False)

    # Store vote into db
    try:
        p = Poll.objects.get(text=pollText)
        pc = PollChoice.objects.get(pollID=p, text=pollChoiceText)
        v = Vote(userID=UserProfile.objects.get(username=username), pollChoiceID=pc)

        p.numVotes += 1
        pc.numVotes += 1

        p.save()
        pc.save()
        v.save()

        # Store a Notification to Poll's owner
        text = "A user voted on your poll!"
        n = Notification(userID=p.userID, pollID=p, type="poll", text=text)
        n.save()

        return JsonResponse({'status': 200,
                         'message': "Successfully added vote for poll choice \'" + pollChoiceText + "\'.",
                         'data': {'poll': pollText }}
                        , status=200)

    # Data already exists
    except IntegrityError:
            return JsonResponse(UNIQUE_400, status=400)

    # User does not exist
    except ObjectDoesNotExist:
            return JsonResponse(USER_400, status=400)