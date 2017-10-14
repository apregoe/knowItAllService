from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from ..models import *
from django.db import IntegrityError
from ..constants import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def createNotification(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400, safe=False)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    username = request.GET.get(username_param)
    type = request.GET.get(type_param)
    title = request.GET.get(title_param)
    text = request.GET.get(text_param)

    # Check if all parameters provided
    if any(var is None for var in [username, type, text]):
        return JsonResponse(createNotification_400_ALL, status=400, safe=False)


    try:
        p = Poll.objects.get(text=title)
    # Poll does not exist
    except ObjectDoesNotExist:
            return JsonResponse(POLL_400, status=400)


    try:
        u = UserProfile.objects.get(username=username)
        n = Notification(userID=u, pollID=p, type=type, text=text)
        n.save()

        return JsonResponse({'status': 200,
                         'message': "Successfully created notification for user " + username + ".",
                         'data': {'type': type, 'text': text }}
                        , status=200)

    # Data already exists
    except IntegrityError:
            return JsonResponse(UNIQUE_400, status=400)

    # User does not exist
    except ObjectDoesNotExist:
            return JsonResponse(USER_400, status=400)