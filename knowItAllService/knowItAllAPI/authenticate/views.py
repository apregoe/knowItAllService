from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import UserProfile
from ..constants import *

def authenticate(request):
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
            # If User already authenticated
            if user.userVerified == True:
                return JsonResponse(authenticate_400_AA, status=400)

            user.userVerified = True
            user.save()
            return JsonResponse({'status': 200,
                         'message': "User authenticated successfully.",
                         'data': {'username': username, 'password': password }}
                        , status=200)

        return JsonResponse(PASSWORD_400, status=400)
    else:
        # Failure
        return JsonResponse(USER_400, status=400)