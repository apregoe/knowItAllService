### Classes

## User
sessionToken_param = 'sessionToken'
email = 'email'
password = 'password'
userVerified = 'userVerified'

## Topic
topic_param = 'topic'
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


### JsonResponse
POST_400 = {'status': 400, 'message': "Error, please use POST."}

## createTopic
createTopic_400_ALL = {'status': 400, 'message': "Error: please provide a topic and a category."}
createTopic_400_C = {'status': 400, 'message': "Error: category must be an int 1-4."}

## createPoll
createPoll_400_ALL = {'status': 400, 'message': "Error, please provide userID, text, choices, and openForever."}
createPoll_400_OF = {'status': 400, 'message': "Error, openForever must be either 'true' or 'false'."}
createPoll_400_DL = {'status': 400, 'message': "Error, dayLimit must be a value > 0."}