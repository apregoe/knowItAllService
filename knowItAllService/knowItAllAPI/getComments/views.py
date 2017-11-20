from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from ..constants import *
from ..serializers import *
from rest_framework.views import APIView


# Get specific poll or topic
class getComments(APIView):
    # GET request
    def get(self, request):
        type = request.GET.get(type_param)
        username = request.GET.get(username_param)
        pollText = request.GET.get(pollText_param)

        # Get comments for a single user or poll
        try:
            if type == 'user':
                u = UserProfile.objects.filter(username=username)
                if len(u) is 0:
                    return JsonResponse(USER_400, status=400)
                u = u.first()
                comment = Comment.objects.filter(userID=u)
                commentSerializer = CommentSerializer(comment, many=True)
                return JsonResponse({'status': 200, 'username': u.username, 'comments': commentSerializer.data}, safe=False)

            elif type == 'poll':
                p = Poll.objects.filter(text=pollText)
                if len(p) is 0:
                    return JsonResponse(POLL_400, status=400)
                p = p.first()
                print(p)
                comment = Comment.objects.filter(pollID=p)
                commentSerializer = CommentSerializer(comment, many=True)
                return JsonResponse({'status': 200, 'poll': p.text, 'comments': commentSerializer.data}, safe=False)

        # Data does not exist
        except ObjectDoesNotExist:
            return JsonResponse(DATA_400, status=400)

    # POST request
    def post(self, request):
        return JsonResponse(GET_400, status=400)

# https://stackoverflow.com/a/23788795