from django.http import JsonResponse
from django.db import IntegrityError
from .models import *
from ..constants import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
# https://stackoverflow.com/a/3711911
def createTags(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    title = request.GET.get(title_param)

    # Check if all parameters provided
    if (title is None):
        return JsonResponse(createTags_400_ALL, status=400)

    # Splitting string into the individual tags
    tagList = title.split(' ')
    for tag in tagList:
        t = Tag(title=tag)
        # Try to store data into db
        try:
            t.save()
            return JsonResponse(createTags_200_ALL, status=200)

        except IntegrityError:
            return JsonResponse(UNIQUE_400, status=400)
