from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db import IntegrityError
from .models import *
from ..constants import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def editProfile(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    username = request.GET.get(username_param)
    newPassword = request.GET.get(newPassword_param)

    try:
        u = UserProfile.objects.get(username=username)
        u.password = newPassword
        u.save()
        return JsonResponse({'status': 200,
                         'message': "Successfully saved new password for user " + username,
                         'data': {'newPassword': newPassword }}
                        , status=200)

    except IntegrityError:
        return JsonResponse(UNIQUE_400, status=400)

    # User does not exist
    except ObjectDoesNotExist:
        return JsonResponse(USER_400, status=400)