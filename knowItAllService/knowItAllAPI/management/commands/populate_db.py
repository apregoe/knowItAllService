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
        self.createTopics()
        self.createPolls()

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
        print("Creating superuser")
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
        self.createPoll(username="shuzawa@usc.edu", text="Best backend Framework?", choices="Django,Ruby on Rails,Spring"
                   , category="1", openForever="1", dayLimit="0", anonymous="0", tags="coding,hack,programmer,cs")

        self.createPoll(username="prego@usc.edu", text="Best Burger Place",
                   choices="Five guys,in n out,fatburger,jack in the box"
                   , category="2", openForever="1", dayLimit="0", anonymous="1", tags="burger,fat,delicious")

        self.createPoll(username="shenjona@usc.edu", text="Who is the best footballer?", choices="sam,adory,messi",
                        category="3", openForever="0", dayLimit="3", anonymous="0", tags="usc,football,athletic")

        self.createPoll(username="filipsan@usc.edu", text="Best college bar at usc?", choices="tommy,901,banditos,bacaro",
                        category="4", openForever="1", dayLimit="0", anonymous="0", tags="usc,bars,drink,nightlife")


    #creates and authenticates user
    def createUser(self, username, password):
        s = UserProfile(username=username, password=password); s.save()
        r = requests.get(self.hostname + "authenticate?username=" + username)
        print(r.text)

    def createPoll(self, username, category, text, choices, openForever, dayLimit, anonymous, tags):
        response = requests.post(self.hostname + 'createPoll?username=' + username + '&category=' + category +
                                 '&text=' + text + '&choices=' + choices + '&openForever=' + openForever
                                 + '&dayLimit=' + dayLimit + "&anonymous=" + anonymous + "&tags=" + tags)
        print(response.text)