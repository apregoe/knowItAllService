from django.conf.urls import url, include
from . import views
# . means importing from current directory

urlpatterns = [
    url(r'^$', views.index, name='index'), # This is the base index for .../api/
    url(r'^register', include('knowItAllAPI.register.urls')), # This is .../api/register
    url(r'^createPoll', include('knowItAllAPI.createPoll.urls')),  # This is .../api/createPoll
    url(r'^createTopic', include('knowItAllAPI.createTopic.urls')),  # This is .../api/createTopic
]
