from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import UserProfile
from ..constants import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def authenticate(request):
    # if request.method != "POST":
    #     return JsonResponse(POST_400, status=400)

    username = request.GET.get(username_param)
    password = request.GET.get(password_param)
    check = request.GET.get(check_param)
    user = UserProfile.objects.filter(username=username)

    # User has an account
    if user.exists():
        user = UserProfile.objects.get(username=username)
        # # Password is correct
        # if user.password == password:
        #     # Only check if user is authenticated but not update values
        if check is not None and check == 'true':
            return JsonResponse({'status': 200,
                     'authenticated': ("true" if user.userVerified else "false") }
                    , status=200)

        # If User already authenticated
        if user.userVerified == True:
            return JsonResponse(authenticate_400_AA, status=400)

        user.userVerified = True
        user.save()
        return JsonResponse({'status': 200,
                     'message': "User authenticated successfully.",
                     'data': {'username': username}}
                    , status=200)

        # return JsonResponse(PASSWORD_400, status=400)
    else:
        # Failure
        return JsonResponse(USER_400, status=400)