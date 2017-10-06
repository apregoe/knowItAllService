from django.db import models
from datetime import datetime, timedelta
'''
    ID for each class will automatically be created; don't need to declare it
    CASCADE = if User is deleted, delete ALL polls linked to him, not just this one
'''

class User(models.Model):
    sessionToken = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    userVerified = models.BooleanField(False)

class Topic(models.Model):
    name = models.CharField(max_length=100) # Ex. CSCI 310, Prof. Michael Schindler
    category = models.CharField(max_length=100) # 1 of the 4: Academic, Entertainment, Social, Location
    avRating = models.DecimalField(max_digits=2, decimal_places=1) # Ex. 4.5 stars
    numReviews = models.IntegerField()

class Review(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    topicID = models.ForeignKey(Topic, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.CharField(max_length=300, default="")
    dateCreated = models.DateTimeField(auto_now_add=True, blank=True)

class Poll(models.Model):
    # def setDeadline(dayLimit):
    #     return datetime.today() + timedelta(days=dayLimit)
    userID = models.ForeignKey(User, on_delete=models.CASCADE) # who owns the poll
    text = models.CharField(max_length=300)
    numVotes = models.IntegerField()
    openForever = models.BooleanField() # will the poll be open forever?
    dayLimit = models.IntegerField() # if False, many days will the poll be open for?
    dateCreated = models.DateTimeField(auto_now_add=True, blank=True)
    startTimeStamp = models.DateTimeField(auto_now_add=True, blank=True)
    # endTimeStamp = models.DateTimeField(default=setDeadline(numDays)) if endTime else None
    # https://stackoverflow.com/a/15289461

# https://docs.djangoproject.com/en/1.11/intro/tutorial02/
class PollChoice(models.Model):
    pollID = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

class Vote(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    pollChoiceID = models.ForeignKey(PollChoice, on_delete=models.CASCADE)

