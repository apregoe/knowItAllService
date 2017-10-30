from django.test import TestCase
from ..constants import *
from ..models import *
import json

'''
    In terminal, cd to 'knowItAllAPI' directory, then call 'python ../manage.py test'
    To check JSON response -> print(response.json())
'''
class MyNotificationsTests(TestCase):
    def setUp(self):
        u = UserProfile.objects.create(username='test@usc.edu', password='test')
        UserProfile.objects.create(username='test2@usc.edu', password='test2')
        c = Category.objects.create(title='c1')
        p = Poll.objects.create(userID=u, categoryID=c, text="pt", numVotes=0,
                                openForever=True, dayLimit=0)
        Notification.objects.create(userID=u, pollID=p, type="poll", text="User voted on poll!")

    def test_myNotifications(self):
        # Not using GET -> 400
        response = self.client.post('/api/myNotifications?username=test@usc.edu')
        self.assertEqual(str(response.json()['message']), GET_400m)

        # Base case not empty -> 200
        response = self.client.get('/api/myNotifications?username=test@usc.edu')
        self.assertNotEqual(response.json()['notifications'], [])

        # Base case empty -> 200
        response = self.client.get('/api/myNotifications?username=test2@usc.edu')
        self.assertEqual(response.json()['notifications'], [])

        # User doesn't exist
        response = self.client.get('/api/myNotifications?username=a@usc.edu')
        self.assertEqual(str(response.json()['message']), USER_400m)


class MyPostsTests(TestCase):
    def setUp(self):
        u = UserProfile.objects.create(username='test@usc.edu', password='test')
        UserProfile.objects.create(username='test2@usc.edu', password='test2')
        c = Category.objects.create(title='c1')
        p = Poll.objects.create(userID=u, categoryID=c, text="pt", numVotes=0,
                                openForever=True, dayLimit=0)
        PollChoice.objects.create(pollID=p, text='pc1')
        PollChoice.objects.create(pollID=p, text='pc2')
        PollChoice.objects.create(pollID=p, text='pc3')

    def test_myPosts(self):
        # Not using GET -> 400
        response = self.client.post('/api/myPosts?username=test2@usc.edu')
        self.assertEqual(str(response.json()['message']), GET_400m)

        # Base case not empty -> 200
        response = self.client.get('/api/myPosts?username=test@usc.edu')
        self.assertNotEqual(response.json()['polls'], [])

        # Base case empty -> 200
        response = self.client.get('/api/myPosts?username=test2@usc.edu')
        self.assertEqual(response.json()['polls'], [])

        # User doesn't exist
        response = self.client.get('/api/myPosts?username=a@usc.edu')
        self.assertEqual(str(response.json()['message']), USER_400m)


class RegisterTests(TestCase):
    def setUp(self):
        u = UserProfile.objects.create(username='test@usc.edu', password='test')

    def test_register(self):
        # Not using POST -> 400
        response = self.client.get('/api/register?username=test2@usc.edu&password=')
        self.assertEqual(str(response.json()['message']), POST_400m)

        # Base case -> 200
        response = self.client.post('/api/register?username=test2@usc.edu&password=')
        self.assertEqual(str(response.json()['message']), register_200m)

        # Not all parameters provided -> 400
        response = self.client.post('/api/register?username=test@usc.edu')
        self.assertEqual(str(response.json()['message']), register_400_UPm)

        # Non-USC email -> 400
        response = self.client.post('/api/register?username=test@test.com&password=')
        self.assertEqual(str(response.json()['message']), register_400_INVm)

        # User already exists -> 400
        response = self.client.post('/api/register?username=test@usc.edu&password=')
        self.assertEqual(str(response.json()['message']), register_400_EXm)


class VoteTests(TestCase):
    def setUp(self):
        u = UserProfile.objects.create(username='test@usc.edu', password='test')
        UserProfile.objects.create(username='test2@usc.edu', password='test2')
        c = Category.objects.create(title='c1')
        p = Poll.objects.create(userID=u, categoryID=c, text="pt", numVotes=0,
                                openForever=True, dayLimit=0)
        PollChoice.objects.create(pollID=p, text='pc1')
        PollChoice.objects.create(pollID=p, text='pc2')
        PollChoice.objects.create(pollID=p, text='pc3')
        # Vote.objects.create(userID=u2, pollChoiceID=p1)

    def test_vote(self):
        # Not using POST -> 400
        response = self.client.get('/api/vote?username=test@usc.edu&pollText=pt'
                                    '&pollChoiceText=pc1')
        self.assertEqual(str(response.json()['message']), POST_400m)

        # Base case -> 200
        response = self.client.post('/api/vote?username=test@usc.edu&pollText=pt'
                                    '&pollChoiceText=pc1')
        self.assertEqual(str(response.json()['message']), vote_200_ADDm)

        # Not all parameters provided -> 400
        response = self.client.post('/api/vote?username=test@usc.edu')
        self.assertEqual(str(response.json()['message']), vote_400_ALLm)

        # User doesn't exist -> 400
        response = self.client.post('/api/vote?username=a@usc.edu&pollText=pt'
                                    '&pollChoiceText=pc1')
        self.assertEqual(str(response.json()['message']), USER_400m)

        # User did vote on this poll -> 200
        response = self.client.post('/api/vote?username=test@usc.edu&pollText=pt')
        self.assertEqual(str(response.json()['message']), vote_200_FDm)

        # User did not vote on this poll -> 404
        response = self.client.post('/api/vote?username=test2@usc.edu&pollText=pt')
        self.assertEqual(str(response.json()['message']), vote_404m)

        # Delete flag is true -> 200
        response = self.client.post('/api/vote?username=test@usc.edu&pollText=pt'
                                    '&pollChoiceText=pc1&deleteVote=1')
        self.assertEqual(str(response.json()['message']), deleteVote_200m)

        # Delete flag is not a digit -> 400
        response = self.client.post('/api/vote?username=test@usc.edu&pollText=pt'
                                    '&pollChoiceText=pc1&deleteVote=string')
        self.assertEqual(str(response.json()['message']), deleteVoteFlag_400_InvalidFlagParamm)

#TODO do we need to test for the password?
class AuthenticateTest(TestCase):
    def setUp(self):
        self.username = 'test@usc.edu'
        u = UserProfile.objects.create(username=self.username, password='test')

    def test_authenticate(self):
        # not using GET -> 400
        response = self.client.post('/api/authenticate?username='+self.username)
        self.assertEqual(response.json(), GET_400)

        # authenticate user check false -> 400
        response = self.client.get('/api/authenticate?username='+self.username+'&check=true')
        self.assertEqual(response.json() ,authenticate_UserCheck("false", self.username))

        # authenticate user base case -> 200
        response = self.client.get('/api/authenticate?username='+self.username)
        self.assertEqual(response.json(), authenticate_UserAuthenticated(self.username))

        # authenticate user check true -> 200
        response = self.client.get('/api/authenticate?username=' + self.username + '&check=true')
        self.assertEqual(response.json(), authenticate_UserCheck("true", self.username))

        #user already verified -> 400
        response = self.client.get('/api/authenticate?username='+self.username)
        self.assertEqual(response.json(), authenticate_400_AA)

        #user does not exists
        response = self.client.get('/api/authenticate?username=notExisting@user.com')
        self.assertEqual(response.json(), USER_400)


class SearchTest(TestCase):
    def setUp(self):
        self.username = 'test@usc.edu'
        u = UserProfile.objects.create(username=self.username, password='test')
        #populate database for searching
        self.client.post('/api/createCategory?populate=true')
        c1 = Category.objects.get(pk=1)
        c2 = Category.objects.get(pk=2)
        c3 = Category.objects.get(pk=3)
        c4 = Category.objects.get(pk=4)
        p = Poll.objects.create(userID=u, categoryID=c1, text="Best backend Framework?", numVotes=0,
                                openForever=True, dayLimit=0)
        PollChoice.objects.create(pollID=p, text='Django')
        PollChoice.objects.create(pollID=p, text='Ruby on Rails')
        PollChoice.objects.create(pollID=p, text='Spring')

        Topic.objects.create(title="Five Guys", category=c2, avRating=0, numReviews=0)
        Topic.objects.create(title="Da Row", category=c3, avRating=0, numReviews=0)
        Topic.objects.create(title="McCarthy Quad", category=c4, avRating=0, numReviews=0)

    def test_Search(self):
        # not using GET -> 400
        response = self.client.post('/api/search?query=backend')
        self.assertEqual(response.json(), GET_400)

        # no query provided
        response = self.client.get('/api/search')
        self.assertEqual(response.json(), search_400_QY)

        # category 1 search
        response = self.client.get('/api/search?query=backend academic')
        self.assertEqual(str(response.json()['data'][0]['text']), "Best backend Framework?")

        # category 2 search
        response = self.client.get('/api/search?query=five guys food')
        self.assertEqual(str(response.json()['data'][0]['title']), "Five Guys")

        #category 3 search
        response = self.client.get('/api/search?query=row entertainment')
        self.assertEqual(str(response.json()['data'][0]['title']), "Da Row")

        #category 4 search
        response = self.client.get('/api/search?query= mccarthy location')
        self.assertEqual(str(response.json()['data'][0]['title']), "McCarthy Quad")


class CreateCategoryTest(TestCase):
    def test_createCategory(self):
        # not using POST-> 400
        response = self.client.get('/api/createCategory')
        self.assertEqual(response.json(), POST_400)

        # populate is None or != true
        response = self.client.post('/api/createCategory')
        self.assertEqual(response.json(), createCategory_400_PO)

        # base case, populate = true
        response = self.client.post('/api/createCategory?populate=true')
        self.assertEqual(response.json(), createCategory_SUCCESS)

        #integrity error, data already exists!
        response = self.client.post('/api/createCategory?populate=true')
        self.assertEqual(response.json(), UNIQUE_400)


class CreateNotificationTest(TestCase):
    def setUp(self):
        self.username = 'test@usc.edu'
        self.client.post('/api/createCategory?populate=true')
        self.type = "poll"
        self.text = "Someone voted on a poll you created."
        self.title = "Best backend Framework?"
        c1 = Category.objects.get(pk=1)
        u = UserProfile.objects.create(username=self.username, password='test')
        p = Poll.objects.create(userID=u, categoryID=c1, text=self.title, numVotes=0,
                                openForever=True, dayLimit=0)
        PollChoice.objects.create(pollID=p, text='Django')
        PollChoice.objects.create(pollID=p, text='Ruby on Rails')
        PollChoice.objects.create(pollID=p, text='Spring')

    def test_createNotification(self):
        #no GET
        response = self.client.get('/api/createNotification')
        self.assertEqual(response.json(), POST_400)

        #missing attributes
        response = self.client.post('/api/createNotification')
        self.assertEqual(response.json(), createNotification_400_ALL)

        #poll does not exists
        response = self.client.post('/api/createNotification?username='+self.username
                                    +'&type=anything&text=Notification message&title=unexisting Poll')
        self.assertEqual(response.json(), POLL_400)

        #notificatino created
        response = self.client.post('/api/createNotification?username='+self.username
                                    +'&type='+self.type+'&text='+self.text+'&title='+self.title)
        self.assertEqual(response.json(), createNotification_SUCCESS(self.username, self.type, self.text))

        #Username does not exists
        response = self.client.post('/api/createNotification?username=unexisting@user.com'+
                                    '&type='+self.type+'&text='+self.text+'&title='+self.title)
        self.assertEqual(response.json(), USER_400)
        self.assertEqual(response.json(), USER_400)