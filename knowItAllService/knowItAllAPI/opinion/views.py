from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from ..models import *
from ..constants import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def opinion(request):
    if request.method != "POST" or request.method != "GET":
        return JsonResponse(POSTGET_400, status=400, safe=False)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    username = request.GET.get(username_param)
    type = request.GET.get(type_param)
    pollText = request.GET.get(pollText_param)
    upvote = request.GET.get(upvote_param) # True or False
    reviewUsername = request.GET.get(reviewUsername_param)
    reviewTopic = request.GET.get(reviewTopic_param)
    deleteFlag = request.GET.get(deleteFlag_param)

    if request.method == "POST":
        # Check if all parameters provided
        if any(var is None for var in [username, type, opinion]):
            return JsonResponse(opinion_400_ALL, status=400, safe=False)

        # User doesn't exist
        u = UserProfile.objects.filter(username=username)
        if u is None:
            return JsonResponse(USER_400, status=400)
        u = u.first()

        # Type is incorrect
        if type != 'poll' or type != 'review':
            return JsonResponse(opinion_400_TP, status=400)

        # Opinion is incorrect
        if upvote != '1' or upvote != '0':
            return JsonResponse(opinion_400_UP, status=400)
        upvote = True if upvote == '1' else False

        o = None
        if type is 'poll':
            p = Poll.objects.filter(text=pollText)
            if p is None:
                return JsonResponse(POLL_400, status=400)
            o = Opinion(userID=u, type='poll', pollID=p.first(), upvote=upvote)

            if deleteFlag is not None:
                Opinion.objects.filter(userID=u, type='poll', pollID=p.first(), upvote=upvote)
                if o is not None:
                    o.first().delete()
                    return JsonResponse(opinion_200_DEL, status=200)
                else:
                    return JsonResponse(opinion_400_DEL, status=200)

        # review
        else:
            ru = UserProfile.objects.filter(username=reviewUsername)
            if ru is None:
                return JsonResponse(USER_400, status=400)
            ru = ru.first()
            t = Topic.objects.filter(title=reviewTopic)
            if t is None:
                return JsonResponse(TOPIC_400, status=400)
            t = t.first()
            o = (Opinion(userID=u, type='review', reviewID=Review.objects.get(userID=ru, topicID=t),upvote=upvote))

            if deleteFlag is not None:
                Opinion.objects.filter(userID=u, type='review', reviewID=Review.objects.get(userID=ru, topicID=t),upvote=upvote)
                if o is not None:
                    o.first().delete()
                    return JsonResponse(opinion_200_DEL, status=200)
                else:
                    return JsonResponse(opinion_400_DEL, status=200)

        try:
            o.save()

        # Poll does not exist
        except ObjectDoesNotExist:
                return JsonResponse(POLL_400, status=400)

        return JsonResponse(opinion_200, status=200, safe=False)

    # GET request
    else:
        # Type is incorrect
        if type != 'poll' or type != 'review':
            return JsonResponse(opinion_400_TP, status=400)

        if type == 'poll':
            p = Poll.objects.filter(text=pollText)
            if p is None:
                return JsonResponse(POLL_400, status=400)
            upvotes = len(Opinion.objects.filter(pollID=p, upvote=True))
            downvotes = len(Opinion.objects.filter(pollID=p, upvote=False))
            return JsonResponse({'status': 200, 'poll': pollText, 'upvotes': upvotes, 'downvotes': downvotes}, safe=False)
        else:
            ru = UserProfile.objects.filter(username=reviewUsername)
            if ru is None:
                return JsonResponse(USER_400, status=400)
            ru = ru.first()
            t = Topic.objects.filter(title=reviewTopic)
            if t is None:
                return JsonResponse(TOPIC_400, status=400)
            t = t.first()
            r = Review.objects.get(userID=ru, topicID=t)
            upvotes = len(Opinion.objects.filter(reviewID=r, upvote=True))
            downvotes = len(Opinion.objects.filter(reviewID=r, upvote=False))
            return JsonResponse({'status': 200, 'reviewUsername': reviewUsername, 'topic': reviewTopic,
                                 'upvotes': upvotes, 'downvotes': downvotes}, safe=False)