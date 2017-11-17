from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from ..models import *
from django.db import IntegrityError
from ..constants import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def opinion(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400, safe=False)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    username = request.GET.get(username_param)
    type = request.GET.get(type_param)
    text = request.GET.get(text_param)
    opinion = request.GET.get(opinion_param)

    # Check if all parameters provided
    if any(var is None for var in [username, type, text, opinion]):
        return JsonResponse(opinion_400_ALL, status=400, safe=False)

    # Check if user exists
    u = None
    try:
        user = UserProfile.objects.get(username=username)
    except ObjectDoesNotExist:
        return JsonResponse(USER_400, status=400)

    try:
        p = Poll.objects.get(text=text)

    # Poll does not exist
    except ObjectDoesNotExist:
            return JsonResponse(POLL_400, status=400)

    return JsonResponse(deleteVoteFlag_200_VoteDeleted(username), status=200, safe=False)