### Classes

## User
username_param = 'username'
password_param = 'password'
userVerified_param = 'userVerified'

## Topic
title_param = 'title'
category_param = 'category'
avRating_param = 'avRating'
numReviews_param = 'numReviews'

## Poll
userID_param = 'userID'
text_param = 'text'
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
# userID_param
pollChoiceID_param = 'pollChoiceID'

## Review
topicTitle_param = 'topicTitle'
rating_param = 'rating'
comment_param = 'comment'


### JsonResponse
POST_400 = {'status': 400, 'message': "Error, please use POST."}
UNIQUE_400 = {'status': 400, 'message': "Error: Data already exists!"}
PASSWORD_400 = {'status': 400, 'message': "Error, user password not correct."}

## login
USER_400 = {'status': 400, 'message': "Error: user does not exist."}

## createTopic
createTopic_400_ALL = {'status': 400, 'message': "Error: please provide a title and category."}
createTopic_400_C = {'status': 400, 'message': "Error: category must be an int 1-4."}

## createPoll
createPoll_400_ALL = {'status': 400, 'message': "Error, please provide username, text, choices, and openForever."}
createPoll_400_OF = {'status': 400, 'message': "Error, openForever must be either 1 (true) or 0 (false)."}
createPoll_400_DL = {'status': 400, 'message': "Error, dayLimit must be a value > 0."}

## createReview
createReview_400_ALL = {'status': 400, 'message': "Error, please provide a username, topicTitle, and rating."}
createReview_400_RT = {'status': 400, 'message': "Error, rating must be a float between 0 and 5."}

## authenticate
authenticate_400_AA = {'status': 400, 'message': "Error, user already authenticated."}

### Categories
CATEGORIES = {
    1: "Academic",
    2: "Food",
    3: "Social",
    4: "Entertainment"
}