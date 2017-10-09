from django.http import JsonResponse
from django.db import IntegrityError
from .models import UserProfile
from ..constants import *

def register(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    username = request.GET.get(username_param)
    password = request.GET.get(password_param)

    u = UserProfile(username=username, password=password)
    try:
        u.save()
        return JsonResponse({'status': 200,
                         'message': "Successfully created user.",
                         'data': {'username': u.username, 'password': password }}
                        , status=200)

    except IntegrityError:
        return JsonResponse(UNIQUE_400, status=400)