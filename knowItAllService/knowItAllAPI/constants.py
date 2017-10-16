### Classes

#email certifications
# knowItAllDomain = "http://127.0.0.1:8000"
knowItAllDomain = "https://0a79ab09.ngrok.io"
knowItAllEmail = 'knowitallusc310@gmail.com'
knowItAllEmailPassword = 'H52-J5K-Wm7-WFb'
def confirmationMessage(username):
    return "Hi!\n\n  Thank you for registering to knowItAll! Please confirm your email clicking in the following link:\n " \
           +knowItAllDomain+"/api/authenticate?username=" + username + "\n\n Thanks!"

## User
username_param = 'username'
password_param = 'password'
check_param = 'check'
userVerified_param = 'userVerified'

## Edit Profile
newPassword_param = 'newPassword'

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


### JsonResponse
GET_400 = {'status': 400, 'message': "Error, please use GET."}
POST_400 = {'status': 400, 'message': "Error, please use POST."}
UNIQUE_400 = {'status': 400, 'message': "Error: Data already exists!"}
def UNIQUE_400_EXISTS(data):
    return {'message': "Error: " + data + " already exists!"}
PASSWORD_400 = {'status': 400, 'message': "Error, user password not correct."}

## general
USER_400 = {'status': 400, 'message': "Error: user does not exist."}
DATA_400 = {'status': 400, 'message': "Error: data does not exist."}
def DATA_400_NOT_EXISTS(data):
    return {'message': "Error: " + data + " do/does not exist."}
POLL_400 = {'status': 400, 'message': "Error: poll does not exist."}


## authenticate
authenticate_400_AA = {'status': 400, 'message': "Error, user already authenticated."}

## createCategory
createCategory_400_PO = {'status': 400, 'message': "Error: populate must be set to 'true'."}

## createTopic
createTopic_400_ALL = {'status': 400, 'message': "Error: please provide a title and category."}
createTopic_400_C = {'status': 400, 'message': "Error: category must be an int 1-4."}

## createPoll
createPoll_400_ALL = {'status': 400, 'message': "Error, please provide username, text, choices, and openForever."}
createPoll_400_OF = {'status': 400, 'message': "Error, openForever must be either 1 (true) or 0 (false)."}
createPoll_400_DL = {'status': 400, 'message': "Error, dayLimit must be a value > 0."}

## deletePoll
deletePoll_400_ALL = {'message': 'Please provide ' + username_param + ', and ' + pollText_param + ' parameters.'}
def deletePoll_USERNAMEISNOTOWNER(username, pollText):
    return {'message': username + ' is not the owner for the poll: ' + pollText}
deletePoll_200_SUCCESS = {'message': 'Poll deleted successfully'}
deletePoll_400_UNSUCCESSFUL = {'message': 'No poll deleted. Reason: Not found'}

## createReview
createReview_400_ALL = {'status': 400, 'message': "Error, please provide a username, topicTitle, and rating."}
createReview_400_RT = {'status': 400, 'message': "Error, rating must be a float between 0 and 5."}

## delete Review
deleteReview_400_INVALID_PARAMS = {'message': 'Plase provide ' + username_param + ', and ' + topicTitle_param}
def  deleteReview_SUCESS(username, topicTitle):
    return {'message': 'Review about:' + topicTitle + ' from: ' + username + '. Has been deleted' }

## createNotification
createNotification_400_ALL = {'status': 400, 'message': "Error, please provide a username, type, and text."}


## vote
vote_400_ALL = {'status': 400, 'message': "Error, please provide a username, pollText, and pollChoiceText."}
deleteVoteFlag_400_InvalidFlagParam = {'message': deleteVoteFlag_param + ' value should be wither 1 or 0.'}
def deleteVoteFlag_200_VoteDeleted (username, voteChoice):
    return  {'message': 'Vote choice: ' + voteChoice + ', from ' + username + ' was successfully deleted'}

## getPost
getPost_400_TP = {'status': 400, 'message': "Error, type must be either 'poll' or 'topic'."}

## getPost
getTrending_400_TP = {'status': 400, 'message': "Error, type must be either 'poll', 'topic', or 'all'."}

## query
search_400_QY = {'status': 400, 'message': "Error, please provide a query."}

#register
registerUser_INVALIDPARAMS = {'message': 'Please provide ' + username_param + ' and ' + password_param}
def register_INVALIDUSER(username):
    return {'message': username + ' is not valid. It should be a valid USC email (Ex. tommy.trojan@usc.edu)'}

### Categories
CATEGORIES = {
    1: "Academic",
    2: "Food",
    3: "Entertainment",
    4: "Location"
}