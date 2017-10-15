from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import *
from django.db import IntegrityError
from ..constants import *
from decimal import Decimal
from ..serializers import *
from collections import OrderedDict
from operator import itemgetter

# __icontains = https://docs.djangoproject.com/en/1.11/ref/models/querysets/#icontains

def search(request):
    if request.method != "GET":
        return JsonResponse(GET_400, status=400, safe=False)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    query = request.GET.get(query_param)

    # Check if query provided
    if query is None:
        return JsonResponse(search_400_QY, status=400, safe=False)

    query = query.lower()
    topics = None
    polls = None
    categoryData = None
    dataCount = {}

    if CATEGORIES.get(1).lower() in query:
        query = query.replace(CATEGORIES.get(1), '')
        topics = Topic.objects.filter(category=Category.objects.get(pk=1))
        polls = Poll.objects.filter(categoryID=Category.objects.get(pk=1))
    elif CATEGORIES.get(2).lower() in query:
        query = query.replace(CATEGORIES.get(2), '')
        topics = Topic.objects.filter(category=Category.objects.get(pk=2))
        polls = Poll.objects.filter(categoryID=Category.objects.get(pk=2))
    elif CATEGORIES.get(3).lower() in query:
        query = query.replace(CATEGORIES.get(3), '')
        topics = Topic.objects.filter(category=Category.objects.get(pk=3))
        polls = Poll.objects.filter(categoryID=Category.objects.get(pk=3))
    elif CATEGORIES.get(4).lower() in query:
        query = query.replace(CATEGORIES.get(4), '')
        topics = Topic.objects.filter(category=Category.objects.get(pk=4))
        polls = Poll.objects.filter(categoryID=Category.objects.get(pk=4))

    # Add all topics underneath selected category to dataCount
    if topics is not None:
        topicsSerializer = TopicSerializer(topics, many=True)
        # category_data = topicsSerializer.data[0]['id'] # Get id of review
        # Store all topics under a category into a dictionary to keep count of 'hits'
        for topic in topicsSerializer.data:
            topicID = topic['id']
            dataCount['topic'+str(topicID)] = 1 # 'Hit' for the first time

    # Add all polls underneath selected category to dataCount
    if polls is not None:
        pollsSerializer = PollSerializer(polls, many=True)
        for poll in pollsSerializer.data:
            pollID = poll['id']
            dataCount['poll' + str(pollID)] = 1  # 'Hit' for the first time

    queryList = query.split(' ')

    for query in queryList:
        if query == '':
            continue

        # Query through all topics
        topics = Topic.objects.filter(title__icontains=query)
        topicsSerializer = TopicSerializer(topics, many=True)
        for topic in topicsSerializer.data:
            topicID = 'topic' + str(topic['id'])
            if topicID not in dataCount:
                dataCount[topicID] = 1 # 'Hit' for the first time
            else:
                dataCount[topicID] += 1

        # Query through all polls
        polls = Poll.objects.filter(text__icontains=query)
        pollsSerializer = PollSerializer(polls, many=True)
        for poll in pollsSerializer.data:
            pollID = 'poll' + str(poll['id'])
            if pollID not in dataCount:
                dataCount[pollID] = 1 # 'Hit' for the first time
            else:
                dataCount[pollID] += 1

    '''
        At this point, dataCount stores all 'hits' of a review/poll.
        dataOrder sorts by decreasing 'hit'.
        dataList returns results in dataOrder, i.e. most relevant to search query.
    '''

    # [('topic2', 3), ('topic1', 2), ('poll1', 1)]
    dataOrder = sorted(dataCount.items(), key=itemgetter(1), reverse=True)
    dataList = []
    for data in dataOrder:
        idNum = data[0]
        if 'topic' in idNum:
            idNum = idNum.replace('topic', '')
            topic = Topic.objects.filter(pk=int(idNum))
            topicSerializer = TopicSerializer(topic, many=True)
            dataList.append(topicSerializer.data[0])
        elif 'poll' in idNum:
            idNum = idNum.replace('poll', '')
            poll = Poll.objects.filter(pk=int(idNum))
            pollSerializer = PollSerializer(poll, many=True)
            dataList.append(pollSerializer.data[0])

    return JsonResponse({'status': 200,
                         'data': dataList}, status=200)
