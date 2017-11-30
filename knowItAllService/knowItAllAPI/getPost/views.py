from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db import IntegrityError
from .models import *
from ..constants import *
import base64
from ..s3Client import *
from ..serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView

# Get specific poll or topic
class getPost(APIView):
    # GET request
    def get(self, request):
        type = request.GET.get(type_param)
        text = request.GET.get(text_param)
        username = request.GET.get(username_param)
        
        try:
            if type == 'topic':
                topic = Topic.objects.filter(title=text)
                topicSerializer = TopicSerializer(topic, many=True)
                reviews = Review.objects.filter(topicID=topic)
                reviewsSerializer = ReviewSerializer(reviews, many=True)
                opinions = []
                uservotes = []
                images =[]
                # getting the image, if there is any
                # imageKey = createReviewKey(username=username, topicTitle=topic)
                # image = getObject(bucketName=bucket_name, key=imageKey)
                for review in reviews:
                    upvotes = len(Opinion.objects.filter(reviewID=review, upvote=True))
                    downvotes = len(Opinion.objects.filter(reviewID=review, upvote=False))
                    opinions.append({'reviewID': review.pk, 'upvotes': upvotes, 'downvotes': downvotes })
                    if username is not None:
                        if len(UserProfile.objects.filter(username=username)) != 0:
                            u = UserProfile.objects.filter(username=username)
                            if len(Opinion.objects.filter(userID=u, reviewID=review)) != 0:
                                uservotes.append({'reviewID': review.pk, 'upvote':
                                    Opinion.objects.get(userID=u, reviewID=review).upvote})
                    #get image data drom s3
                    # getting the image, if there is any
                    imageKey = createReviewKey(username=review.username, topicTitle=text)
                    image = getObject(bucketName=bucket_name, key=imageKey)
                    if image != "":
                        # with open("image.png", "wb") as fh:
                        #     fh.write(image)
                        images.append({'reviewID': review.pk, 'image': image})

                return JsonResponse({'status': 200, 'topic': topicSerializer.data, 'reviews': reviewsSerializer.data,
                                     'opinions': opinions, 'uservotes': uservotes, 'images':images}, safe=False)

            elif type == 'poll':
                poll = Poll.objects.filter(text=text)
                pollSerializer = PollSerializer(poll, many=True)
                pc = PollChoice.objects.filter(pollID=poll)
                pcSerializer = PollChoiceSerializer(pc, many=True)
                return JsonResponse({'status': 200, 'poll': pollSerializer.data, 'pc': pcSerializer.data }, safe=False)

            # Type is incorrect
            else:
                return JsonResponse(getPost_400_TP, status=400)
        # Data does not exist
        except ObjectDoesNotExist:
            return JsonResponse(DATA_400, status=400)

    # POST request
    def post(self, request):
        return JsonResponse(GET_400, status=400)

# https://stackoverflow.com/a/23788795