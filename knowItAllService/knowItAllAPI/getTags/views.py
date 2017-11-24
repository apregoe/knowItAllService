from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from ..models import *
from ..constants import *
from rest_framework.views import APIView


# Get specific poll or topic
class getTags(APIView):
    # GET request
    def get(self, request):
        startsWith = request.GET.get(startsWith_param)

        if startsWith is None:
            return JsonResponse(getTags_400, status=400)

        # Get tags that match firstLetters
        try:
            allTags = Tag.objects.all()
            startsWithTags = []
            for tag in allTags:
                if tag.title.startswith(startsWith):
                    startsWithTags.append(tag.title)
            # TODO(Nico): Sort these by popularity once the intial code works.

            return JsonResponse({'status': 200, 'tags': ",".join(startsWithTags)}, safe=False)

        # Data does not exist
        except ObjectDoesNotExist:
            return JsonResponse(DATA_400, status=400)

    # POST request
    def post(self, request):
        return JsonResponse(GET_400, status=400)


