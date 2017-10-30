from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import UserProfile
from ..constants import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def authenticate(request):
    # for key, value in request.GET.items():
    #     print ("%s %s" % (key, value))

    if request.method != "GET":
        return JsonResponse(GET_400, status=400)

    username = request.GET.get(username_param)
    password = request.GET.get(password_param)
    check = request.GET.get(check_param)
    user = UserProfile.objects.filter(username=username)

    # User has an account
    if user.exists():
        user = UserProfile.objects.get(username=username)

        # Check if password is correct
        if password is not None:
            if user.password == password:
                return JsonResponse(authenticate_UserLoggedIn(username=username, password=password)
                        , status=200)
            else:
                return JsonResponse(PASSWORD_400, status=400)

        #     # Only check if user is authenticated but not update values
        if check is not None and check == 'true':
            isVerified = ""
            if user.userVerified:
                isVerified="true"
            else:
                isVerified="false"
            return JsonResponse({'status': 200,
                     'authenticated': (isVerified) }
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
        #using json is easier for testing
        # return HttpResponse("<h1>Authentication Success!</h1>"
        #                     "<h2>Your email \'"+username+"\' has been authenticated. Please login on your device.</h2>")

        # return JsonResponse(PASSWORD_400, status=400)
    else:
        # Failure
        return JsonResponse(USER_400, status=400)