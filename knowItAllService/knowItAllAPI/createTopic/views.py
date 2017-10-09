from django.shortcuts import render
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Topic
from ..constants import *

# https://stackoverflow.com/a/3711911
def createTopic(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    topic = request.GET.get(topic_param)
    category = request.GET.get(category_param)

    # Check if all parameters provided
    if (topic==None or category==None):
        return JsonResponse(createTopic_400_ALL, status=400)

    # Check if category is valid
    if not category.isdigit() or not (1 <= int(category) <= 4):
        return JsonResponse(createTopic_400_C, status=400)
    category = int(category)

    # Store data into db
    t = Topic(name=topic,category=category, avRating=0, numReviews=0)
    try:
        t.save()
        return JsonResponse({'status': 200,
                         'message': "Successfully created topic.",
                         'data': {'topic': t.name, 'category': CATEGORIES.get(t.category)}}
                        , status=200)

    except IntegrityError:
        return JsonResponse(UNIQUE_400, status=400)
