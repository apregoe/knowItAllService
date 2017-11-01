from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import *
from ..constants import *
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def editPost(request):
    if request.method != 'POST':
        return JsonResponse(POST_400, status=400, safe=False)

    username = request.GET.get(username_param)
    type = request.GET.get(type_param)

    try:
        u = UserProfile.objects.filter(username=username)
        if len(u) == 0:
            return JsonResponse(editProfile_400_INV, status=400)

        if type == 'review':
            topic = request.GET.get(topicTitle_param)
            newRating = request.GET.get(rating_param)
            newComment = request.GET.get(comment_param)

            # Check if all parameters provided
            if any(var is None for var in [newRating, newComment]):
                return JsonResponse(editPost_400_RV, status=400, safe=False)

            # Check if rating is float
            if not isfloat(newRating):
                return JsonResponse(createReview_400_RT, status=400, safe=False)
            else:
                newRating = float(newRating)
            if not (0 <= newRating <= 5):
                return JsonResponse(createReview_400_RT, status=400, safe=False)

            print(topic)
            topic = Topic.objects.get(title=topic)
            user = UserProfile.objects.get(username=username)
            review = Review.objects.get(userID=user, topicID=topic)
            print(review.rating)
            review.rating = newRating
            review.comment = newComment
            review.save()

            return JsonResponse(editPost_200_RV(username, newRating, newComment), safe=False)

        # elif type == 'poll':
        # ...

        # Type is incorrect
        else:
            return JsonResponse(editPost_400_TP, status=400)

    # Data does not exist
    except ObjectDoesNotExist:
        return JsonResponse(DATA_400, status=400)


# Check if value is float
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False