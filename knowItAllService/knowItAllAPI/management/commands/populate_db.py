from django.core.management.base import BaseCommand
import requests
import os
from ...models import *

class Command(BaseCommand):
    # > python manage.py help populate_db
    help = 'This is the help string'
    # hostname = "http://knowitalllive-dev.us-west-1.elasticbeanstalk.com/api/"
    hostname = "http://127.0.0.1:8000/api/"

    # 'main' function
    def handle(self, *args, **options):
        self.setUp()
        self.createCategories()
        self.createUsers()
        # self.createPolls()
        # self.createTopics()

    def setUp(self):
        # removing the database
        os.system("rm db.sqlite3")
        # removing migration files and creating __init__.py
        os.system("rm -rf knowItAllAPI/migrations/*")
        # We cannot delete __init__.py
        os.system("git checkout knowItAllAPI/migrations/__init__.py")
        # makemigrations and migrate
        os.system("python manage.py makemigrations")
        os.system("python manage.py migrate")
        # creating superuser
        os.system("python manage.py createsuperuser")

    def createCategories(self):
        # create categories
        print("Creating categories...")
        response = requests.post(self.hostname + "createCategory?populate=true")
        print(response.text)

    def createUsers(self):
        self.createUser("shuzawa@usc.edu", "12345")
        self.createUser("filipsan@usc.edu", "12345")
        self.createUser("prego@usc.edu", "12345")
        self.createUser("shenjona@usc.edu", "12345")

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

    #creates and authenticates user
    def createUser(self, username, password):
        s = UserProfile(username=username, password=password); s.save()
        r = requests.get(self.hostname + "authenticate?username=" + username)
        print(r.text)