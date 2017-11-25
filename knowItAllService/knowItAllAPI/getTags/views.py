from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from ..models import *
from ..constants import *
from rest_framework.views import APIView


# Get specific poll or topic
class getTags(APIView):
    # GET request
    def get(self, request):
        startsWithString = request.GET.get(startsWith_param)

        if startsWithString is None:
            return JsonResponse(getTags_400, status=400)

        # Get tags that match firstLetters
        try:
            startsWithTags = Tag.objects.filter(title__startswith=startsWithString)

            # Make a map from tag to number of links for the tag.
            startsWithDict = {}
            for tag in startsWithTags:
                links = TagLinker.objects.filter(tagID = tag)
                startsWithDict[tag.title] = links.count()

            startWithList = startsWithDict.items()
            sortedList = sorted(startWithList, key=lambda x : (x[1], x[0]))
            sortedTags = [t[0] for t in sortedList]

            return JsonResponse({'status': 200, 'tags': ",".join(sortedTags)}, safe=False)

        # Data does not exist
        except ObjectDoesNotExist:
            return JsonResponse(DATA_400, status=400)

    # POST request
    def post(self, request):
        return JsonResponse(GET_400, status=400)


