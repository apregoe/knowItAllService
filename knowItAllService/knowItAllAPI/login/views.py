from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import UserProfile
from ..constants import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400)

    username = request.GET.get(username_param)
    password = request.GET.get(password_param)
    user = UserProfile.objects.filter(username=username)

    # User has an account
    if user.exists():
        user = UserProfile.objects.get(username=username)

        # Password is correct
        if user.password == password:
            return JsonResponse({'status': 200,
                         'message': "User logged in successfully.",
                         'data': {'username': username, 'password': password }}
                        , status=200)
        else:
            return JsonResponse(PASSWORD_400, status=400)
    else:
        # Failure
        return JsonResponse(USER_400, status=400)