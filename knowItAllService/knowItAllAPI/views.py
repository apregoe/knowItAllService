from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("<h2>This is the stub for KnowItAll's API calls.</h2>")