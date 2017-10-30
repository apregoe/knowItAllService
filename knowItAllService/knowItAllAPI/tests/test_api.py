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

class CreatePollTest(TestCase):
    def setUp(self):
        self.username = 'test@usc.edu'
        self.category = "1"
        self.text = "Best backend Framework?"
        self.choices = "Django,Ruby on Rails,Spring"
        self.openForever = '1'
        self.dayLimit = '10'
        self.client.post('/api/createCategory?populate=true')
        UserProfile.objects.create(username=self.username, password='test')

    def test_createPoll(self):
        #no GET
        response = self.client.get('/api/createPoll')
        self.assertEqual(response.json(), POST_400)

        #missing attributes
        response = self.client.post('/api/createPoll')
        self.assertEqual(response.json(), createPoll_400_ALL)

        #category not valid
        response = self.client.post('/api/createPoll?username='+self.username+'&category=notValidCategory'
                                    '&text='+self.text+'&choices='+self.choices+'&openForever='+self.openForever+
                                    '&dayLimit='+self.dayLimit)
        self.assertEqual(response.json(), createTopic_400_C)

        #open forever not digit
        response = self.client.post('/api/createPoll?username='+self.username+'&category='+self.category+
                                    '&text='+self.text+'&choices='+self.choices+'&openForever=notDigit'+
                                    '&dayLimit='+self.dayLimit)
        self.assertEqual(response.json(), createPoll_400_OF)

        #openForever is digit but not a valid one
        self.openForever = '3'
        response = self.client.post('/api/createPoll?username=' + self.username + '&category=' + self.category +
                                    '&text=' + self.text + '&choices=' + self.choices + '&openForever='+self.openForever +
                                    '&dayLimit=' + self.dayLimit)
        self.assertEqual(response.json(), createPoll_400_OF)

        #dayLimit < 0
        self.openForever = "0"
        self.dayLimit = "-1"
        response = self.client.post('/api/createPoll?username=' + self.username + '&category=' + self.category +
                                    '&text=' + self.text + '&choices=' + self.choices + '&openForever='+self.openForever +
                                    '&dayLimit=' + self.dayLimit)
        self.assertEqual(response.json(), createPoll_400_DL)

        #base case to create poll
        self.openForever = "1"
        self.dayLimit = "0"
        response = self.client.post('/api/createPoll?username=' + self.username + '&category=' + self.category +
                                    '&text=' + self.text + '&choices=' + self.choices + '&openForever='+self.openForever
                                     + '&dayLimit=' + self.dayLimit)
        self.assertEqual(response.json(), createPoll_SUCCESS(self.text, self.choices.split(',')))

        #data already exists
        response = self.client.post('/api/createPoll?username=' + self.username + '&category=' + self.category +
                                    '&text=' + self.text + '&choices=' + self.choices + '&openForever='+self.openForever
                                    + '&dayLimit=' + self.dayLimit)
        self.assertEqual(response.json(), UNIQUE_400)

        # #user does not exists
        #TODO this gives me an error:
        #TODO django.db.transaction.TransactionManagementError: An error occurred in the current transaction. You can't
        #TODO execute queries until the end of the 'atomic' block.
        # self.username = "notExistingUser"
        # response = self.client.post('/api/createPoll?username=' + self.username + '&category=' + self.category +
        #                             '&text=' + self.text + '&choices=' + self.choices + '&openForever='+self.openForever
        #                             + '&dayLimit=' + self.dayLimit)
        # self.assertEqual(response.json(), USER_400)


class CreateReviewTest(TestCase):
    def setUp(self):
        self.username = 'test@usc.edu'
        self.topicTitle = "Five Guys"
        self.rating = '4'
        self.comment = "Good but nothing like in n out"
        self.client.post('/api/createCategory?populate=true')
        c2 = Category.objects.get(pk=2)#food
        UserProfile.objects.create(username=self.username, password='test')
        Topic.objects.create(title=self.topicTitle, category=c2, avRating=0, numReviews=0)

    def test_createReview(self):
        #not a GET request
        response = self.client.get('/api/createReview')
        self.assertEqual(response.json(), POST_400)

        #no attributes
        response = self.client.post('/api/createReview')
        self.assertEqual(response.json(), createReview_400_ALL)

        #rating is not float
        self.rating = 'notFloat'
        response = self.client.post('/api/createReview?username='+self.username+'&topicTitle='+
                                    self.topicTitle+'&rating='+self.rating+'&comment='+self.comment)
        self.rating = '4'

        #Create review success
        response = self.client.post('/api/createReview?username='+self.username+'&topicTitle='+
                                    self.topicTitle+'&rating='+self.rating+'&comment='+self.comment)
        self.assertEqual(response.json(), createReview_SUCCESS(self.topicTitle, float(self.rating), self.comment))

        #integrity error, data exists
        response = self.client.post('/api/createReview?username='+self.username+'&topicTitle='+
                                    self.topicTitle+'&rating='+self.rating+'&comment='+self.comment)
        self.assertEqual(response.json(), UNIQUE_400)

        #user object does not exists
        #TODO this gives me an error:
        #TODO django.db.transaction.TransactionManagementError: An error occurred in the current transaction. You can't
        #TODO execute queries until the end of the 'atomic' block.
        # self.username = "notExistingUser"
        # response = self.client.post('/api/createReview?username='+self.username+'&topicTitle='+
        #                                     self.topicTitle+'&rating='+self.rating+'&comment='+self.comment)
        # self.assertEqual(response.json(), USER_400)



class CreateTopicTest(TestCase):
    def setUp(self):
        self.title = "Five Guys"
        self.category = '1'
        self.client.post('/api/createCategory?populate=true')

    def test_createTopic(self):
        #no a GET request
        response = self.client.get('/api/createTopic')
        self.assertEqual(response.json(), POST_400)

        #no attributes
        response = self.client.post('/api/createTopic')
        self.assertEqual(response.json(), createTopic_400_ALL)

        #category not valid
        self.category="notValidCategory"
        response = self.client.post('/api/createTopic?title='+self.title+'&category='+self.category)
        self.assertEqual(response.json(), createTopic_400_C)
        self.category = '1'

        #success case
        response = self.client.post('/api/createTopic?title='+self.title+'&category='+self.category)
        self.assertEqual(response.json(), createTopic_SUCCESS(self.title, CATEGORIES.get(int(self.category))))

        #topic already exists
        response = self.client.post('/api/createTopic?title='+self.title+'&category='+self.category)
        self.assertEqual(response.json(), UNIQUE_400)

class DeletePollTest(TestCase):
    def setUp(self):
        self.username = 'test@usc.edu'
        self.username2 = 'test2@usc.edu'
        self.pollText = "Best backend Framework?"
        self.client.post('/api/createCategory?populate=true')

        u = UserProfile.objects.create(username=self.username, password='test')
        UserProfile.objects.create(username=self.username2, password='test')

        c1 = Category.objects.get(pk=1)
        p = Poll.objects.create(userID=u, categoryID=c1, text=self.pollText, numVotes=0,
                                openForever=True, dayLimit=0)
        PollChoice.objects.create(pollID=p, text='Django')
        PollChoice.objects.create(pollID=p, text='Ruby on Rails')
        PollChoice.objects.create(pollID=p, text='Spring')

    def test_deletePoll(self):
        #not a get request
        response = self.client.get('/api/deletePoll')
        self.assertEqual(response.json(), POST_400)

        #no attributes
        response = self.client.post('/api/deletePoll')
        self.assertEqual(response.json(), deletePoll_400_ALL)

        #user not the owner
        response = self.client.post('/api/deletePoll?username='+self.username2+
                                    '&pollText='+self.pollText)
        self.assertEqual(response.json(), deletePoll_USERNAMEISNOTOWNER(self.username2, self.pollText))

        #poll deleted success
        response = self.client.post('/api/deletePoll?username='+self.username+
                                '&pollText='+self.pollText)
        self.assertEqual(response.json(), deletePoll_200_SUCCESS)

        #poll or user that does not exists
        self.pollText = "Not existing poll"
        response = self.client.post('/api/deletePoll?username='+self.username+
                                '&pollText='+self.pollText)
        self.assertEqual(response.json(), DATA_400_NOT_EXISTS(self.pollText + ' or ' + self.username))


class DeleteReview(TestCase):
    def setUp(self):
        self.username = 'test@usc.edu'
        self.username2 = 'test2@usc.edu'
        self.topicTitle = "Five Guys"
        self.rating = '4'
        self.category = '2'
        self.comment = "Good but nothing like in n out"
        self.client.post('/api/createCategory?populate=true')

        userId = UserProfile.objects.create(username=self.username, password='test')
        UserProfile.objects.create(username=self.username2, password='test')
        c2 = Category.objects.get(pk=2)
        topicId = Topic.objects.create(title=self.topicTitle, category=c2, avRating=0, numReviews=0)

        # self.client.post('/api/createTopic?title='+self.topicTitle+'&category='+self.category)
        self.client.post('/api/createReview?username='+self.username+'&topicTitle='+self.topicTitle+
                         '&rating='+self.rating+'&comment='+self.comment)


    def test_deleteReview(self):
        #not a get request
        response = self.client.get('/api/deleteReview')
        self.assertEqual(response.json(), POST_400)

        #no attributes
        response = self.client.post('/api/deleteReview')
        self.assertEqual(response.json(), deleteReview_400_INVALID_PARAMS)

        # review deleted success
        response = self.client.post('/api/deleteReview?username=' + self.username +
                                    '&topicTitle=' + self.topicTitle)
        self.assertEqual(response.json(), deleteReview_SUCESS(self.username, self.topicTitle))

        #review or user that does not exists
        self.topicTitle= "Not existing topic"
        response = self.client.post('/api/deleteReview?username='+self.username+
                                '&topicTitle='+self.topicTitle)
        self.assertEqual(response.json(), DATA_400_NOT_EXISTS(self.topicTitle + ', or ' + self.username))

        #user has no review in this topic
        self.topicTitle = "Five Guys"
        response = self.client.post('/api/deleteReview?username=' + self.username2 +
                                    '&topicTitle=' + self.topicTitle)
        self.assertEqual(response.json(), deletePoll_USERNAMEISNOTOWNER(self.username2, self.topicTitle))

