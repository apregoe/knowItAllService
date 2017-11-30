from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import UserProfile, Topic, Review
from django.db import IntegrityError
from ..constants import *
from ..s3Client import *
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def createReview(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400, safe=False)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    username = request.GET.get(username_param)
    topicTitle = request.GET.get(topicTitle_param)
    rating = request.GET.get(rating_param)
    comment = request.GET.get(comment_param)
    anonymous = request.GET.get(anonymous_param)
    imageFlag = request.GET.get(image_param)

    # Check if all parameters provided
    if any(var is None for var in [username, topicTitle, rating, anonymous, imageFlag]):
        return JsonResponse(createReview_400_ALL, status=400, safe=False)

    # Check if rating is float
    if not isfloat(rating):
        return JsonResponse(createReview_400_RT, status=400, safe=False)
    else:
        rating = float(rating)
    if not (0 <= rating <= 5):
        return JsonResponse(createReview_400_RT, status=400, safe=False)

    # Check if imageFlag is int 0<=x<=1
    if not imageFlag.isdigit() or not (0 <= int(imageFlag) <= 1):
        return JsonResponse(createReview_400_Image, status=400)
    imageFlag = int(imageFlag)

    #check anonymous value is 1 or 0
    if not anonymous.isdigit() or not (0 <= int(anonymous) <= 1):
        return JsonResponse(ANONYMOUS_400, status=400)
    anonymous = int(anonymous)

    anonymousToStore = False
    # Store poll into db
    if anonymous == 1:
        anonymousToStore = True

    try:
        t = Topic.objects.get(title=topicTitle)
        userId=UserProfile.objects.get(username=username)

        imageS3Path = "/" + username + "/" + topicTitle + "/"
        fileName = reviewImageFilename
        if imageFlag == 1:#store image in s3
            #parsing the body
            body = json.loads(request.body)
            image = body['image']
            saveFile(bucketName=bucket_name, path=imageS3Path, fileName=fileName, fileBinary=image)
            getObject(bucketName=bucket_name, path=imageS3Path, fileName="text.txt")

        r = Review(userID=userId, topicID=t, rating=rating, comment=comment, username=username, anonymous=anonymousToStore)
        r.save()
        # Update review value
        t.avRating = ((t.avRating * t.numReviews) + Decimal.from_float(rating))/(t.numReviews+1)
        t.numReviews += 1
        t.save()

        return JsonResponse(createReview_SUCCESS(topicTitle, rating, comment)
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

def isInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False