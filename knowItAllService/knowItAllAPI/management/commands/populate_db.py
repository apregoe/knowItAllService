from django.core.management.base import BaseCommand
from ...models import *

class Command(BaseCommand):
    # > python manage.py help populate_db
    help = 'This is the help string'

    # 'main' function
    def handle(self, *args, **options):
        self.createCategories()
        self.createUsers()
        self.createTopics()
        self.createPolls()

    def createCategories(self):
        a = Category(title='Academic'); a.save()
        f = Category(title='Food'); f.save()
        e = Category(title='Entertainment'); e.save()
        l = Category(title='Location'); l.save()

    def createUsers(self):
        s = UserProfile(username="shuzawa@usc.edu", password="12345"); s.save()
        s = UserProfile(username="filipsan@usc.edu", password="12345"); s.save()
        s = UserProfile(username="aprego@usc.edu", password="12345"); s.save()
        s = UserProfile(username="shenjona@usc.edu", password="12345"); s.save()

    def createTopics(self):
        t = Topic(title="EE 109", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        t = Topic(title="CSCI 103", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        t = Topic(title="CSCI 109", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        t = Topic(title="CSCI 104", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        t = Topic(title="CSCI 170", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        t = Topic(title="CSCI 201", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        t = Topic(title="CSCI 270", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        t = Topic(title="CSCI 310", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        t = Topic(title="CSCI 356", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        t = Topic(title="CSCI 350", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        t = Topic(title="CSCI 360", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()

        t = Topic(title="Blaze Pizza", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()
        t = Topic(title="Panda Express", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()
        t = Topic(title="CAVA", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()
        t = Topic(title="The Habit Burger and Grill", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()
        t = Topic(title="Chipotle", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()
        t = Topic(title="EVK", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()
        t = Topic(title="Cafe 84", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()
        t = Topic(title="Parkside Dining Hall", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()

        t = Topic(title="Wonder Woman", category=Category.objects.get(pk=3), avRating=0, numReviews=0); t.save()
        t = Topic(title="USC Football", category=Category.objects.get(pk=3), avRating=0, numReviews=0); t.save()
        t = Topic(title="URB-E", category=Category.objects.get(pk=3), avRating=0, numReviews=0); t.save()

        t = Topic(title="Leavey Library", category=Category.objects.get(pk=4), avRating=0, numReviews=0); t.save()
        t = Topic(title="Lyon Center", category=Category.objects.get(pk=4), avRating=0, numReviews=0); t.save()
        t = Topic(title="Village Gym", category=Category.objects.get(pk=4), avRating=0, numReviews=0); t.save()
        t = Topic(title="SAL", category=Category.objects.get(pk=4), avRating=0, numReviews=0); t.save()

    def createPolls(self):
        p = Poll(userID=UserProfile.objects.get(username="shenjona@usc.edu"), categoryID=Category.objects.get(pk=1),
                 text="Who is the best teammate?", numVotes=0, openForever=True, dayLimit=0,
                 username="shuzawa", anonymous=False)
        p = Poll(userID=UserProfile.objects.get(username="shenjona@usc.edu"), categoryID=Category.objects.get(pk=1),
                 text="Who is the best teammate?", numVotes=0, openForever=True, dayLimit=0,
                 username="shuzawa", anonymous=False)
        p = Poll(userID=UserProfile.objects.get(username="shenjona@usc.edu"), categoryID=Category.objects.get(pk=1),
                 text="Who is the best teammate?", numVotes=0, openForever=True, dayLimit=0,
                 username="shuzawa", anonymous=False)
        p = Poll(userID=UserProfile.objects.get(username="shenjona@usc.edu"), categoryID=Category.objects.get(pk=1),
                 text="Who is the best teammate?", numVotes=0, openForever=True, dayLimit=0,
                 username="shuzawa", anonymous=False)

        p.save()
        # Store each choice into db
        cList = choices.split(',')
        for choice in cList:
            c = PollChoice(pollID=p, text=choice)
            c.save()