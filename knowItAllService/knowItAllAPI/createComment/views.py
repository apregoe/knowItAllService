from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import *
from django.db import IntegrityError
from ..constants import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def createComment(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400, safe=False)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    username = request.GET.get(username_param)
    pollText = request.GET.get(pollText_param)
    comment = request.GET.get(comment_param)
    anonymous = request.GET.get(anonymous_param)

    # Check if anonymous = 0 or 1
    if not anonymous.isdigit() or not (0 <= int(anonymous) <= 1):
        return JsonResponse(createReview_400_ANONYMOUS_INVALID, status=400)
    anonymous = int(anonymous)
    anonymous = True if anonymous is '1' else False

    # Check if all parameters provided
    if any(var is None for var in [username, pollText, comment]):
        return JsonResponse(createReview_400_ALL, status=400, safe=False)

    try:
        u=UserProfile.objects.get(username=username)
        p=Poll.objects.get(text=pollText)
        c = Comment(userID=u, pollID=p, text=comment, username=username, anonymous=anonymous)
        c.save()

        return JsonResponse(createComment_200_ALL, status=200)
    # Data already exists
    except IntegrityError:
            return JsonResponse(UNIQUE_400, status=400)

    # User does not exist
    except ObjectDoesNotExist:
            return JsonResponse(USER_400, status=400)
