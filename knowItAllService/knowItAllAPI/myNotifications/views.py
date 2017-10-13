from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db import IntegrityError
from ..models import *
from ..constants import *
from ..serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView

# Lists all posts of user
class myNotifications(APIView):
    # GET request
    def get(self, request):
        username = request.GET.get(username_param)
        try:
            user = UserProfile.objects.get(username=username)
            notifications = Notification.objects.filter(userID=user)

            notificationsSerializer = NotificationSerializer(notifications, many=True)
            return JsonResponse({'notifications': notificationsSerializer.data}, safe=False)

        # Data already exists
        except IntegrityError:
            return JsonResponse(UNIQUE_400, status=400)

        # User does not exist
        except ObjectDoesNotExist:
            return JsonResponse(USER_400, status=400)

    # POST request
    def post(self, request):
        return JsonResponse(GET_400, status=400)

# https://stackoverflow.com/a/23788795