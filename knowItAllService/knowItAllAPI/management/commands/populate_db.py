from django.core.management.base import BaseCommand
from threading import Timer
from ...models import *
import requests
import signal
import time
import multiprocessing as mp
import subprocess
import os
import sys

def runLocalServer():
    # runing server in local machine
    os.environ['DJANGO_SETTINGS_MODULE'] = 'knowItAllService.settings'
    os.system('python manage.py runserver')

class Command(BaseCommand):
    # > python manage.py populate_db
    help = 'This is the help string'
    hostname = "http://127.0.0.1:8000/api/"

    # 'main' function
    def handle(self, *args, **options):
        #the setup has to be before running the server because it resets the database
        self.setUp()
        # creating two processes
        # runserver process
        serverProcess = mp.Process(target=runLocalServer, args=())
        serverProcess.start()

        #I sleep enough time to let the server be created, and then I populate the database
        time.sleep(3)
        self.createCategories()
        self.createUsers()
        self.createTopics()
        self.createPolls()
        self.createVotes()
        self.createReviews()

        #finishing server process
        print("Hit ctrl+c")
        serverProcess.join()

    def setUp(self):
        # removing the database
        os.system("rm db.sqlite3")
        # removing migration files and creating __init__.py
        os.system("rm -rf knowItAllAPI/migrations/*")
        # We cannot delete __init__.py
        os.system("touch knowItAllAPI/migrations/__init__.py")
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
        self.createUser("prego@usc.edu", "12345")
        self.createUser("shuzawa@usc.edu", "12345")
        self.createUser("filipsan@usc.edu", "12345")
        self.createUser("shenjona@usc.edu", "12345")

    def createPolls(self):
        self.createPoll(username="shuzawa@usc.edu", text="Best backend Framework?", choices="Django,Ruby on Rails,Spring"
                   , category="1", openForever="1", dayLimit="0", anonymous="0", tags="coding,hack,programmer,cs")

        self.createPoll(username="prego@usc.edu", text="Best Burger Place",
                   choices="Five guys,in n out,fatburger,jack in the box"
                   , category="2", openForever="1", dayLimit="0", anonymous="1", tags="burger,fat,delicious")

        self.createPoll(username="shenjona@usc.edu", text="Who is the best footballer?", choices="sam,adory,messi",
                        category="3", openForever="0", dayLimit="3", anonymous="0", tags="usc,football,athletic")

        self.createPoll(username="filipsan@usc.edu", text="Best college bar at usc?", choices="tradis,901,banditos,bacaro",
                        category="4", openForever="1", dayLimit="0", anonymous="0", tags="usc,bars,drink,nightlife")

    def createVotes(self):
        self.vote("prego@usc.edu","Best backend Framework?","Ruby on Rails")
        self.vote("prego@usc.edu","Best Burger Place","in n out")
        self.vote("prego@usc.edu","Who is the best footballer?","messi")
        self.vote("prego@usc.edu","Best college bar at usc?","901")

        self.vote("shuzawa@usc.edu","Best backend Framework?","Django")
        self.vote("shuzawa@usc.edu","Best Burger Place","fatburger")
        self.vote("shuzawa@usc.edu","Who is the best footballer?","messi")
        self.vote("shuzawa@usc.edu","Best college bar at usc?","banditos")

        self.vote("filipsan@usc.edu", "Best backend Framework?","Spring")
        self.vote("filipsan@usc.edu", "Best Burger Place", "jack in the box")
        self.vote("filipsan@usc.edu", "Who is the best footballer?", "messi")
        self.vote("filipsan@usc.edu", "Best college bar at usc?", "bacaro")

        self.vote("shenjona@usc.edu", "Best backend Framework?", "Django")
        self.vote("shenjona@usc.edu", "Best Burger Place", "in n out")
        self.vote("shenjona@usc.edu", "Who is the best footballer?", "messi")
        self.vote("shenjona@usc.edu", "Best college bar at usc?", "tradis")

    def createTopics(self):

        #It does not create tags
        # t = Topic(title="EE 109", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        # t = Topic(title="CSCI 103", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        # t = Topic(title="CSCI 109", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        # t = Topic(title="CSCI 104", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        # t = Topic(title="CSCI 170", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        # t = Topic(title="CSCI 201", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        # t = Topic(title="CSCI 270", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        # t = Topic(title="CSCI 310", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        # t = Topic(title="CSCI 356", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        # t = Topic(title="CSCI 350", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        # t = Topic(title="CSCI 360", category=Category.objects.get(pk=1), avRating=0, numReviews=0); t.save()
        self.createTopic("EE 109", "1", "ee,hell,hard classes")
        self.createTopic("CSCI 103", "1", "cs,cool classes,easy classes")
        self.createTopic("CSCI 109", "1", "cs,cool classes")
        self.createTopic("CSCI 104", "1", "cs,cool classes")
        self.createTopic("CSCI 170", "1", "cs,cool classes")
        self.createTopic("CSCI 201", "1", "cs,alright classes")
        self.createTopic("CSCI 270", "1", "cs,hard classes")
        self.createTopic("CSCI 310", "1", "cs,cool classes")
        self.createTopic("CSCI 356", "1", "cs,hard classes")
        self.createTopic("CSCI 360", "1", "cs,cool classes")

        # t = Topic(title="Blaze Pizza", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()
        # t = Topic(title="Panda Express", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()
        # t = Topic(title="CAVA", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()
        # t = Topic(title="The Habit Burger and Grill", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()
        # t = Topic(title="Chipotle", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()
        # t = Topic(title="EVK", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()
        # t = Topic(title="Cafe 84", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()
        # t = Topic(title="Parkside Dining Hall", category=Category.objects.get(pk=2), avRating=0, numReviews=0); t.save()
        self.createTopic("Blaze Pizza", "2", "food,pizza,tasty,fat food")
        self.createTopic("Panda Express", "2", "food,americanized asian food,fast food")
        self.createTopic("CAVA", "2", "fast food,white people")
        self.createTopic("The Habit Burger and Grill", "2", "burgers,fat food")
        self.createTopic("Chipotle", "2", "food,americanized mexican food")
        self.createTopic("EVK", "2", "food,dining hall")
        self.createTopic("Cafe 84", "2", "food,dining hall,rip")
        self.createTopic("Parkside Dining Hall", "2", "food,dining hall,10000 miles away")

        #
        #
        # t = Topic(title="Wonder Woman", category=Category.objects.get(pk=3), avRating=0, numReviews=0); t.save()
        # t = Topic(title="USC Football", category=Category.objects.get(pk=3), avRating=0, numReviews=0); t.save()
        # t = Topic(title="URB-E", category=Category.objects.get(pk=3), avRating=0, numReviews=0); t.save()
        self.createTopic("Wonder Woman", "3", "movies,pretty woman,superhero")
        self.createTopic("USC Football", "3", "pac12,football, college football")
        self.createTopic("URB-E", "3", "athletes,transportation,money")

        #
        # t = Topic(title="Leavey Library", category=Category.objects.get(pk=4), avRating=0, numReviews=0); t.save()
        # t = Topic(title="Lyon Center", category=Category.objects.get(pk=4), avRating=0, numReviews=0); t.save()
        # t = Topic(title="Village Gym", category=Category.objects.get(pk=4), avRating=0, numReviews=0); t.save()
        # t = Topic(title="SAL", category=Category.objects.get(pk=4), avRating=0, numReviews=0); t.save()
        self.createTopic("Leavey Library", "4", "stinks,ew,library")
        self.createTopic("Lyon Center", "4", "gym,recreation center")
        self.createTopic("Village Gym", "4", "gym, cool gym, new gym, village")
        self.createTopic("SAL", "4", "cs-majors lost souls, office hours")


    def createReviews(self):
        self.createReview("prego@usc.edu","CSCI 103","5","Great and challenging for noobs.", "0")
        self.createReview("shuzawa@usc.edu", "CSCI 103", "2", "at least is better than youtube", "1")
        self.createReview("filipsan@usc.edu", "CSCI 103", "4", "Great class", "1")
        self.createReview("shenjona@usc.edu", "CSCI 103", "5", "Best class ever", "0")

        self.createReview("prego@usc.edu", "Cafe 84", "5", "It will always be in my heart", "0")
        self.createReview("shuzawa@usc.edu", "Cafe 84", "4", "RIP", "1")
        self.createReview("filipsan@usc.edu", "Cafe 84", "4", "Best crepes ever", "0")
        self.createReview("shenjona@usc.edu", "Cafe 84", "0", "Found a worm once ew", "1")

        self.createReview("prego@usc.edu", "URB-E", "5", "I just bought an URB-E, I am an athlete!", "0")
        self.createReview("shuzawa@usc.edu", "URB-E", "4", "U even URB-E bruh?", "1")
        self.createReview("filipsan@usc.edu", "URB-E", "1", "Bad service", "1")
        self.createReview("shenjona@usc.edu", "URB-E", "3", "Efficient, but I look like a clown", "1")

        self.createReview("prego@usc.edu", "Leavey Library", "0", "Smells like public toilet", "0")
        self.createReview("shuzawa@usc.edu", "Leavey Library", "1", "It is really bad", "1")
        self.createReview("filipsan@usc.edu", "Leavey Library", "1", "Never going back", "1")
        self.createReview("shenjona@usc.edu", "Leavey Library", "5", "Smells like flowers!", "0")

        self.createReview("prego@usc.edu", "Village Gym", "5", "Best gym ever, no joke", "0")
        self.createReview("shuzawa@usc.edu", "Village Gym", "5", "I workout because of this gym", "1")
        self.createReview("filipsan@usc.edu", "Village Gym", "5", "I do not want to graduate because of this gym", "1")
        self.createReview("shenjona@usc.edu", "Village Gym", "1", "Not for me", "1")

        self.createReview("prego@usc.edu", "CSCI 310", "5", "Best TAs ever!", "1")
        self.createReview("shuzawa@usc.edu", "CSCI 310", "5", "Best professor ever!", "1")
        self.createReview("filipsan@usc.edu", "CSCI 310", "5", "Best grading system ever!", "1")
        self.createReview("shenjona@usc.edu", "CSCI 310", "5", "Best class ever!", "1")

    def createTopic(self, title, category, tags):
        response = requests.post(self.hostname+"createTopic?title="+title+"&category="+category+"&tags="+tags)
        print(response.text)

    def createReview(self, username, topicTitle, rating, comment, anonymous):
        response = requests.post(self.hostname + "createReview?username="+username+"&topicTitle="+topicTitle+
                                 "&rating="+rating+"&comment="+comment+"&anonymous="+anonymous)
        print(response.text)

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

    def vote(self, username, pollText, choice):
        response = requests.post(self.hostname + "vote?pollText="+pollText+"&username="+username+"&pollChoiceText="+choice)
        print(response.text)

