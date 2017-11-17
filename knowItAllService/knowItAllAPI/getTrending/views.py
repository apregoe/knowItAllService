from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import *
from django.db import IntegrityError
from ..constants import *
from decimal import Decimal
from ..serializers import *
from collections import OrderedDict
from operator import itemgetter


# Lists all posts of user
def getTrending(request):
    if request.method != "GET":
        return JsonResponse(GET_400, status=400, safe=False)

    try:
        type = request.GET.get(type_param)
        if type == 'topic':
            topic = Topic.objects.all()
            topicSerializer = TopicSerializer(topic, many=True)
            return JsonResponse({'status': 200, 'data': topicSerializer.data}, safe=False)

        elif type == 'poll':
            poll = Poll.objects.all()
            pollSerializer = PollSerializer(poll, many=True)
            return JsonResponse({'status': 200, 'data': pollSerializer.data}, safe=False)

        elif type == 'tags':
            try:
                number = int(request.GET.get(number_param))
            except ValueError:
                return JsonResponse(getTrending_400_NB, status=400)

            tag = Tag.objects.all().order_by('-id')[:number]
            tagSerializer = TagSerializer(tag, many=True)
            return JsonResponse({'status': 200, 'data': tagSerializer.data}, safe=False)

        elif type == 'all':
            topic = Topic.objects.all()
            topicSerializer = TopicSerializer(topic, many=True)
            poll = Poll.objects.all()
            pollSerializer = PollSerializer(poll, many=True)
            return JsonResponse({'status': 200, 'data': topicSerializer.data + pollSerializer.data}, safe=False)

        # Type is incorrect
        else:
            return JsonResponse(getTrending_400_TP, status=400)

    # Data does not exist
    except ObjectDoesNotExist:
        return JsonResponse(DATA_400, status=400)