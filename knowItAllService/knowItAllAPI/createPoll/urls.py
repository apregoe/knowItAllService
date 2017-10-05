from django.conf.urls import url, include
from . import views

# . means importing from current directory

urlpatterns = [
    url(r'^$', views.index) # This is the base index for .../api/createPoll
]
