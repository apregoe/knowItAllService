from django.http import JsonResponse
from django.db import IntegrityError
from .models import UserProfile
from ..constants import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    username = request.GET.get(username_param)
    password = request.GET.get(password_param)

    if any(var is None for var in[username, password]):
        return JsonResponse(registerUser_INVALIDPARAMS, safe=False, status=400)

    #is username valid?
    #1. check if it's a usc email
    #   1.1 Contains the usc.edu domain
    #   1.2 email actually works (PING the email)
    #2. check if username already exists in database

    #1.1 Contains usc.edu domain
    uscDomain = "@usc.edu"
    uscDomainLenght = len(uscDomain)
    isUserValid = False
    if username[-uscDomainLenght:] == uscDomain:
        # 1.2 email actually works (PING the email)
        isUserValid = True
    else:
        #does not contain @usc.edu as the domain
        return JsonResponse(register_INVALIDUSER(username), status=400, safe=False)

    u = UserProfile(username=username, password=password)
    try:
        u.save()
        return JsonResponse({'status': 200,
                         'message': "Successfully created user.",
                         'data': {'username': u.username, 'password': password }}
                        , status=200)

    except IntegrityError:
        return JsonResponse(UNIQUE_400, status=400)