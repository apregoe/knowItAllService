from django.http import JsonResponse
from .models import *
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from ..constants import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def createCategory(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400, safe=False)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    populate = request.GET.get(populate_param)

    # Check if populate is true
    if populate is None or populate != 'true':
        return JsonResponse(createCategory_400_PO, status=400, safe=False)

    # Store poll into db
    try:
        a = Category(title='Academic'); a.save()
        f = Category(title='Food'); f.save()
        e = Category(title='Entertainment'); e.save()
        l = Category(title='Location'); l.save()

        return JsonResponse(createCategory_SUCCESS, status=200)

    # Data already exists
    except IntegrityError:
            return JsonResponse(UNIQUE_400, status=400)