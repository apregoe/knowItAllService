### Classes

#email certifications
# knowItAllDomain = "http://127.0.0.1:8000/api"
# knowItAllDomain = "https://0a79ab09.ngrok.io/api"
knowItAllDomain = "knowItAllLive-dev.us-west-1.elasticbeanstalk.com"
knowItAllEmail = 'knowitallusc310@gmail.com'
knowItAllEmailPassword = 'H52-J5K-Wm7-WFb'
def confirmationMessage(username):
    return "Hi "+username[:-8].capitalize()+"!\n\nThank you for signing up for KnowItAll! Please confirm your email clicking the following link:\n\n " \
           +knowItAllDomain+"/api/authenticate?username="+username+"\n\nBest,\nKnowItAll Team"
def changePassMessage(username, newPassword):
    return "Hi "+username[:-8].capitalize()+"!\n\nPlease confirm your password change by clicking the following link:\n\n " \
           +knowItAllDomain+"/api/editProfile?username="+username+"&newPassword="+newPassword+"\n\nBest,\nKnowItAll Team"

## User
username_param = 'username'
password_param = 'password'
check_param = 'check'
userVerified_param = 'userVerified'

## Edit Profile
newPassword_param = 'newPassword'
forgot_param = 'forgot'

## Category
populate_param = 'populate'

## Topic
title_param = 'title'
type_param = 'type'
category_param = 'category'
avRating_param = 'avRating'
numReviews_param = 'numReviews'

## Poll
userID_param = 'userID'
text_param = 'text'
pollText_param = 'pollText'
numVotes_param = 'numVotes'
openForever_param = 'openForever'
dayLimit_param = 'dayLimit'
dateCreated_param = 'dayCreated'
startTimeStamp_param = 'startTimeStamp'

## Poll Choice
pollID_param = 'pollID'
choices_param = 'choices'
# text_param

## Vote
pollChoiceID_param = 'pollChoiceID'
pollChoiceText_param = 'pollChoiceText'
deleteVoteFlag_param = 'deleteVote'
# username_param

## Review
topicTitle_param = 'topicTitle'
rating_param = 'rating'
comment_param = 'comment'

## Search
query_param = 'query'
searchByTag_param = 'searchByTag'

## anonymous
anonymous_param = 'anonymous'

## Tag
tags_param = 'tags'

## getTrending
number_param = 'number'

# opinion
upvote_param = 'upvote'
reviewUsername_param = 'reviewUsername'
reviewTopic_param = 'reviewTopic'
deleteFlag_param = 'deleteFlag'

# getTags
startsWith_param = "startsWith"

### JsonResponse
GET_400 = {'status': 400, 'message': "Error, please use GET."}
POST_400 = {'status': 400, 'message': "Error, please use POST." }
POSTGET_400 = {'status': 400, 'message': "Error, please use POST or GET." }
UNIQUE_400 = {'status': 400, 'message': "Error: Data already exists!" }
def UNIQUE_400_EXISTS(data):
    return {'status': 400, 'message': "Error: " + data + " already exists!"}
PASSWORD_400 = {'status': 400, 'message': "Error, user password not correct."}
ANONYMOUS_400 = {'status': 400, 'message:' : 'Error, anonymous should be 0 or 1.'}

## general
USER_400 = {'status': 400, 'message': "Error: user does not exist." }
DATA_400 = {'status': 400, 'message': "Error: data does not exist." }
def DATA_400_NOT_EXISTS(data):
    return {'message': "Error: " + data + " do/does not exist."}
POLL_400 = {'status': 400, 'message': "Error: poll does not exist." }
TOPIC_400 = {'status': 400, 'message': "Error: topic does not exist." }

## authenticate
authenticate_400_AA = {'status': 400, 'message': "Error, user already authenticated."}

## createCategory
createCategory_400_PO = {'status': 400, 'message': "Error: populate must be set to 'true'."}
createCategory_SUCCESS = {'status': 200,
                      'message': "Successfully created categories Academic, Food, Entertainment, and Location." }


## createTopic
createTopic_400_ALL = {'status': 400, 'message': "Error: please provide a title, category, username, and tags."}
createTopic_400_C = {'status': 400, 'message': "Error: category must be an int 1-4."}
def createTopic_SUCCESS(title, category, tags):
    return {'status': 200,
     'message': "Successfully created topic.",
     'data': {'title': title, 'category': category, 'tags': tags }}

# createPoll
createPoll_400_ALL = {'status': 400, 'message': "Error, please provide username, text, choices, anonymous, openForever, and tags."}
createPoll_400_OF = {'status': 400, 'message': "Error, openForever must be either 1 (true) or 0 (false)."}
createPoll_400_DL = {'status': 400, 'message': "Error, dayLimit must be a value > 0."}
def createPoll_SUCCESS(pollTitle, choices, tags):
    return {'status': 200,
            'message': "Successfully created poll.",
            'data': {'Poll': pollTitle, 'choices': choices, 'tags': tags }}


## deletePoll
deletePoll_400_ALL = {'message': 'Please provide ' + username_param + ', and ' + pollText_param + ' parameters.'}
def deletePoll_USERNAMEISNOTOWNER(username, pollText):
    return {'message': username + ' is not the owner for the poll: ' + pollText}
deletePoll_200_SUCCESS = {'message': 'Poll deleted successfully'}
deletePoll_400_UNSUCCESSFUL = {'message': 'No poll deleted. Reason: Not found'}

## createReview
createReview_400_ALL = {'status': 400, 'message': "Error, please provide a username, topicTitle, anonymous, and rating."}
createReview_400_RT = {'status': 400, 'message': "Error, rating must be a float between 0 and 5."}
def createReview_SUCCESS(topicTitle, rating, comment):
    return {'status': 200,
     'message': "Successfully created review for topic " + topicTitle + ".",
     'data': {'rating': rating, 'comment': comment}}

## delete Review
deleteReview_400_INVALID_PARAMS = {'message': 'Plase provide ' + username_param + ', and ' + topicTitle_param}
def  deleteReview_SUCESS(username, topicTitle):
    return {'message': 'Review about:' + topicTitle + ' from: ' + username + '. Has been deleted' }
def deleteReview_USERHASNOREVIEWONTHISTOPIC(username, topicTitle):
    return {'message': username + ' has no review for ' + topicTitle}

## createNotification
createNotification_400_ALL = {'status': 400, 'message': "Error, please provide a username, type, and text."}
def createNotification_SUCCESS(username, type, text):
    return {'status': 200,
            'message': "Successfully created notification for user " + username + ".",
            'data': {'type': type, 'text': text }}

## editProfile
editProfile_400_EX = {'status': 400, 'message': "Error, user already exists." }
editProfile_400_UP = {'status': 400, 'message': "Error, user password not correct." }
editProfile_400_INV = {'status': 400, 'message': "Error: user does not exist." }
def editProfile_200_UPD(username, newPassword):
    return {'status': 200, 'message': "Successfully saved new password for user " + username,
            'data': {'newPassword': newPassword} }
def editProfile_200_EM(username, newPassword):
    return {'status': 200, 'message': "Successfully sent email confirmation to update password.",
            'data': {'username': username, 'newPassword': newPassword}}

## editPost
editPost_400_TP = {'status': 400, 'message': "Error, type must be either 'poll' or 'review'."}
editPost_400_RV = {'status': 400, 'message': "Error, please provide rating, anonymous and comment."}
def editPost_200_RV(username, rating, comment):
    return {'status': 200, 'message': "Successfully updated review for user "+username+'!',
            'data': {'newRating': rating, 'newComment': comment } }

## getTrending
getTrending_400_TP = {'status': 400, 'message': "Error, type must be either 'poll', 'topic', or 'all'."}
getTrending_400_NB = {'status' : 400, 'message:' : 'Error, number should be an int >= 1.'}


## getPost
getPost_400_TP = {'status': 400, 'message': "Error, type must be either 'poll' or 'topic'."}

## login
login_400_EXm = "Error, user already exists."
login_400_EX = {'status': 400, 'message': login_400_EXm}
login_400_UPm = "Error, user password not correct."
login_400_UP = {'status': 400, 'message': login_400_UPm}
login_400_INVm = "Error: user does not exist."
login_400_INV = {'status': 400, 'message': login_400_INVm}
def login_200(username,password):
    return {'status': 200, 'message': "User logged in successfully.",
            'data': {'username': username, 'password': password}}

## vote
vote_USERm = "A user voted on your poll!"
vote_404 = {'status': 404, 'message': "No votes found for user on poll." }
vote_400_ALL = {'status': 400, 'message': "Error, please provide a username, pollText, and pollChoiceText." }
deleteVoteFlag_400_InvalidFlagParam = {'message': deleteVoteFlag_param + " should be either 1 or 0." }
def vote_200_ADD(poll, pc):
    return {'status': 200, 'message': "Successfully added vote for poll choice!", 'data': {'poll': poll, 'pc': pc} }
deleteVote_200m = "Vote was successfully deleted!"
def vote_200_FD (pc): return {'status': 200, 'message': "Vote found for user.", 'pc': pc}
def deleteVoteFlag_200_VoteDeleted (username, voteChoice):
    return {'status': 200, 'message': deleteVote_200m, 'data': {'username': username, 'vote': voteChoice}}

# query
search_400_QY = {'status': 400, 'message': "Error, please provide a query."}
def searchByTag_400_NoMatchForTags(tags):
    return {'status': 400, 'message': "No match for the tags: " + str(tags)}

# register
register_400_EX = {'status': 400, 'message': "Error, user already exists."}
register_400_UP = {'status': 400, 'message': "Please provide a username and password."}
register_400_INV = {'status': 400, 'message': "Error, username should be a valid USC email (Ex. tommy.trojan@usc.edu)."}
register_200m = "Successfully created user."
def register_200(username,password):
    return {'status': 200, 'message': register_200m,
            'data': {'username': username, 'password': password}}

# authenticate
def authenticate_UserLoggedIn(username, password):
    return {'status': 200,
            'message': "User logged in successfully.",
            'data': {'username': username, 'password': password }}

def authenticate_UserAuthenticated(username):
    return {'status': 200,
            'message': "User authenticated successfully.",
            'data': {'username': username}}

def authenticate_UserCheck(isVerified, username, password):
    return {'status': 200,
            'username': username,
            'password': password,
            'authenticated': str(isVerified)}

# createTags
createTags_400_ALL = {'status': 400, 'message': "Error: please provide one or more tag titles."}
createTags_200_ALL = {'status': 200, 'message': "Tag successfully stored in DB."}

# createComment
createComment_400_ALL = {'status': 400, 'message': "Error: please provide a username, pollText, and comment."}
createComment_200_ALL = {'status': 200, 'message': "Comment successfully stored."}

# getTags
getTags_400 = {'status': 400, 'message': "Error: please provide startsWith letters."}

# opinion
opinion_400_ALL = {'status': 400, 'message': "Error: please provide username, type, and opinion."}
opinion_400_TP = {'status': 400, 'message': "Error, type must be either poll or review. "}
opinion_400_UP = {'status': 400, 'message': "Error, upvote must be either 1 or 0. "}
opinion_400_DEL = {'status': 200, 'message': "Error, opinion does not exist." }
opinion_200 = {'status': 200, 'message': "Successfully created opinion." }
opinion_200_DEL = {'status': 200, 'message': "Successfully deleted opinion." }
opinion_400_EX = {'status': 400, 'message': "Error, opinion already exists." }

# Categories
CATEGORIES = {
    1: "Academic",
    2: "Food",
    3: "Entertainment",
    4: "Location"
}

