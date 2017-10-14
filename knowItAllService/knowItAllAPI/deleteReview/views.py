from django.shortcuts import render
from ..models import Review
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from ..constants import *

def deleteReview(request):
    return JsonResponse({'message': 'testing deleteReview'}, status=200)