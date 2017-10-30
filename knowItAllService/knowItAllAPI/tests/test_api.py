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

class AuthenticateTest(TestCase):
    def setUp(self):
        self.username = 'test@usc.edu'
        u = UserProfile.objects.create(username=self.username, password='test')

    def test_authenticate(self):
        # not using GET
        response = self.client.post('/api/authenticate?username='+self.username)
        self.assertEqual(response.json(), GET_400)

        response = self.client.get('/api/authenticate?username='+self.username)
        print(response.json(), authenticate_UserAuthenticated(self.username))