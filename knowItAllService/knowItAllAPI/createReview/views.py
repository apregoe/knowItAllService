from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import UserProfile, Topic, Review
from django.db import IntegrityError
from ..constants import *
from decimal import Decimal

def createReview(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400, safe=False)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    username = request.GET.get(username_param)
    topicTitle = request.GET.get(topicTitle_param)
    rating = request.GET.get(rating_param)
    comment = request.GET.get(comment_param)

    # Check if all parameters provided
    if any(var is None for var in [username, topicTitle, rating]):
        return JsonResponse(createReview_400_ALL, status=400, safe=False)

    # Check if rating is float
    if not isfloat(rating):
        return JsonResponse(createReview_400_RT, status=400, safe=False)
    else:
        rating = float(rating)
    if not (0 <= rating <= 5):
        return JsonResponse(createReview_400_RT, status=400, safe=False)

    # Store poll into db

    try:
        t = Topic.objects.get(title=topicTitle)
        r = Review(userID=UserProfile.objects.get(username=username), topicID=t, rating=rating, comment=comment)
        r.save()
        # Update review value
        t.avRating = ((t.avRating * t.numReviews) + Decimal.from_float(rating))/(t.numReviews+1)
        t.numReviews += 1
        t.save()

        return JsonResponse({'status': 200,
                         'message': "Successfully created review for topic " + topicTitle + ".",
                         'data': {'rating': rating, 'comment': comment }}
                        , status=200)
    # Data already exists
    except IntegrityError:
            return JsonResponse(UNIQUE_400, status=400)

    # User does not exist
    except ObjectDoesNotExist:
            return JsonResponse(USER_400, status=400)

# Check if value is float
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False