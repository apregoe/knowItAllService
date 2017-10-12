from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
'''
    ID for each class will automatically be created, don't need to declare it; called pk (primary key)
    CASCADE     -> if User is deleted, delete ALL polls linked to him, not just this one
    CSRFToken   -> https://stackoverflow.com/a/36131930
    POST=empty  -> https://stackoverflow.com/questions/34570145/request-post-get-always-returning-none
    blank=True  -> field not required
    null=True   -> field set to NULL
    unique=True -> non-duplicate entries
    Adding days -> https://stackoverflow.com/a/15289461
'''

# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
#     userVerified = models.BooleanField(default=False)
#     def __str__(self):
#         return self.email +  " -- " + ("Verified" if self.userVerified else "Not Verified")

# https://stackoverflow.com/a/16125609
# Fully customizable User class based off AbstractUser
class UserProfile(AbstractUser):
    userVerified = models.BooleanField(default=False)
    def __str__(self):
        return self.username +  " -- " + ("Verified" if self.userVerified else "Not Verified")

class Topic(models.Model):
    title = models.CharField(max_length=200, default='', unique=True) # Ex. CSCI 310, Prof. Michael Schindler
    category = models.CharField(max_length=200, default='') # 1 of the 4: Academic, Entertainment, Social, Location
    avRating = models.DecimalField(max_digits=2, decimal_places=1) # Ex. 4.5 stars
    numReviews = models.IntegerField()
    def __str__(self):
        return self.title

class Review(models.Model):
    userID = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    topicID = models.ForeignKey(Topic, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.CharField(max_length=200, default='', null=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.topicID.title + " -- " + str(self.rating) + " brains"
    # User can only create one review per topic
    class Meta:
        unique_together = (('userID', 'topicID'))

class Poll(models.Model):
    # def setDeadline(dayLimit):
    #     return datetime.today() + timedelta(days=dayLimit)
    userID = models.ForeignKey(UserProfile, on_delete=models.CASCADE) # who owns the poll
    text = models.CharField(max_length=200, default='', unique=True)
    numVotes = models.IntegerField(default=0)
    openForever = models.BooleanField(default=True) # will the poll be open forever?
    dayLimit = models.IntegerField(default=0) # if False, many days will the poll be open for?
    dateCreated = models.DateTimeField(auto_now_add=True, null=True)
    startTimeStamp = models.DateTimeField(auto_now_add=True, null=True)
    # endTimeStamp = models.DateTimeField(default=setDeadline(numDays)) if endTime else None
    # https://stackoverflow.com/a/15289461
    def __str__(self):
        return self.text

# https://docs.djangoproject.com/en/1.11/intro/tutorial02/
class PollChoice(models.Model):
    pollID = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, default='', unique=True)
    def __str__(self):
        return self.pollID.text + " -- " + self.text

class Vote(models.Model):
    userID = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pollChoiceID = models.ForeignKey(PollChoice, on_delete=models.CASCADE)
    def __str__(self):
        return self.pollChoiceID.text + " -- User " + self.userID.email

# notifications
# Read/unread
