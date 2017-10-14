from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from ..models import *
from django.db import IntegrityError
from ..constants import *
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def vote(request):
    if request.method != "POST":
        return JsonResponse(POST_400, status=400, safe=False)

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    username = request.GET.get(username_param)
    pollText = request.GET.get(pollText_param)
    pollChoiceText = request.GET.get(pollChoiceText_param)

    #flag for delete the vote
    deleteVoteFlag = request.GET.get(deleteVoteFlag_param)

    # Check if all parameters provided
    if any(var is None for var in [username, pollText, pollChoiceText]):
        return JsonResponse(vote_400_ALL, status=400, safe=False)

    # Store vote into db
    saveVote = False
    if deleteVoteFlag != None:
        if deleteVoteFlag.isdigit():
            if deleteVoteFlag == '1':
                #delete vote flag
                saveVote = False
            elif deleteVoteFlag == '0':
                # save the vote (do nothing)
                saveVote = True
            else:
                # deleteVoteFlag is optional but it has to be value 1 or 0
                return JsonResponse (deleteVoteFlag_400_InvalidFlagParam, status= 400, safe = False)

    #retreiving poll and pollchoice from db
    try:
        p = Poll.objects.get(text=pollText)
        pc = PollChoice.objects.get(pollID=p, text=pollChoiceText)
        user = UserProfile.objects.get(username=username)

    # Data already exists
    except IntegrityError:
            return JsonResponse(UNIQUE_400, status=400)

    # User does not exist
    # Todo this will also be called if pollText does not exists. Fix
    except ObjectDoesNotExist:
            return JsonResponse(USER_400, status=400)

    if saveVote == True:
        # if no exceptions in try, then save
        v = Vote(userID=user, pollChoiceID=pc)

        p.numVotes += 1
        pc.numVotes += 1
        try:
            p.save()
            pc.save()
            v.save()

            # Store a Notification to Poll's owner
            text = "A user voted on your poll!"
            n = Notification(userID=p.userID, pollID=p, type="poll", text=text)
            n.save()

        except IntegrityError:
            return JsonResponse(UNIQUE_400_EXISTS("Vote: " + pollChoiceText + " in Poll: " + pollText), status=400)

        return JsonResponse({'status': 200,
                             'message': "Successfully added vote for poll choice \'" + pollChoiceText + "\'.",
                             'data': {'poll': pollText}}
                            , status=200)
    else:
        #delete vote
        try:
            voteToDelete = Vote.objects.get(userID=user, pollChoiceID=pc)
            voteToDelete.delete()

        except ObjectDoesNotExist:
            return JsonResponse(DATA_400_NOT_EXISTS("Vote: " + pollChoiceText + " in Poll: " + pollText), status=400)

        p.numVotes -= 1
        pc.numVotes -= 1

        return JsonResponse(deleteVoteFlag_200_VoteDeleted(username, pollChoiceText), status=200, safe=False)