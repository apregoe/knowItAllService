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
    if any(var is None for var in [username, pollText]):
        return JsonResponse(vote_400_ALL, status=400, safe=False)

    # Check if user exists
    u = None
    try:
        user = UserProfile.objects.get(username=username)
    except ObjectDoesNotExist:
        return JsonResponse(USER_400, status=400)

    # Check if user voted on poll
    if pollChoiceText is None:
        try:
            p = Poll.objects.get(text=pollText)
            pcs = PollChoice.objects.filter(pollID=p)
            v = None
            for pc in pcs:
                v = Vote.objects.filter(userID=user, pollChoiceID=pc)
                if v: break

            if not v:
                return JsonResponse({'status': 404, 'message': "No votes found for user on poll." } , status=200)

            else:
                return JsonResponse({'status': 200, 'message': "Vote found for user.", 'pc': v[0].pollChoiceID.text } , status=200)

        # Poll does not exist
        except ObjectDoesNotExist:
            return JsonResponse(POLL_400, status=400)


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

    # Poll does not exist
    except ObjectDoesNotExist:
            return JsonResponse(POLL_400, status=400)

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
        p.save()
        pc.save()

        return JsonResponse(deleteVoteFlag_200_VoteDeleted(username, pollChoiceText), status=200, safe=False)