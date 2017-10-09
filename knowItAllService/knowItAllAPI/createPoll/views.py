from django.shortcuts import render
from django.http import JsonResponse
from .models import Poll, PollChoice
from ..constants import *

def createPoll(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400, safe=False)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    userID = int(request.GET.get(userID_param))
    text = request.GET.get(text_param)
    choices = request.GET.get(choices_param)
    openForever = request.GET.get(openForever_param)
    dayLimit = request.GET.get(dayLimit_param)

    # Check if all parameters provided
    if any(var is None for var in [userID, text, choices, openForever]):
        return JsonResponse(createPoll_400_ALL, status=400, safe=False)

    # Check if time parameters are correct
    if openForever != 'true' or openForever != 'false':
        return JsonResponse(createPoll_400_OF, status=400, safe=False)
    # Check if dayLimit is filled out correctly
    elif openForever == 'false' and (dayLimit == None or not dayLimit.isdigit() or int(dayLimit) < 1):
        return JsonResponse(createPoll_400_DL, status=400, safe=False)
    else:
        dayLimit = 0
        openForever = True if openForever=='true' else False

    # Store poll into db
    p = Poll(userID=userID, text=text, numVotes=0, openForever=openForever, dayLimit=dayLimit)
    p.save()

    # Store each choice into db
    for choice in choices.split(','):
        c = PollChoice(pollID=p.pk, text=choice)
        c.save()

   # userID = models.ForeignKey(User, on_delete=models.CASCADE) # who owns the poll
   #  text = models.CharField(max_length=300)
   #  numVotes = models.IntegerField()
   #  openForever = models.BooleanField() # will the poll be open forever?
   #  dayLimit = models.IntegerField() # if False, many days will the poll be open for?
   #  dateCreated = models.DateTimeField(auto_now_add=True, blank=True)
   #  startTimeStamp = models.DateTimeField(auto_now_add=True, blank=True)
   #
   #      def get_deadline():
   #          return datetime.today() + timedelta(days=20)
   #
   #      class Bill(models.Model):
   #          name = models.CharField(max_length=50)
   #          customer = models.ForeignKey(User, related_name='bills')
   #          date = models.DateField(default=datetime.today)
   #          deadline = models.DateField(default=get_deadline)