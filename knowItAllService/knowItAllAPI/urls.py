from django.conf.urls import url, include
from . import views
# . means importing from current directory

urlpatterns = [
    url(r'^$', views.index, name='index'), # This is the base index for .../api/

    url(r'^register', include('knowItAllAPI.register.urls')), # This is .../api/register
    url(r'^login', include('knowItAllAPI.login.urls')),
    url(r'^authenticate', include('knowItAllAPI.authenticate.urls')),
    url(r'^editProfile', include('knowItAllAPI.editProfile.urls')),

    url(r'^createCategory', include('knowItAllAPI.createCategory.urls')),
    url(r'^createPoll', include('knowItAllAPI.createPoll.urls')),
    url(r'^createTopic', include('knowItAllAPI.createTopic.urls')),
    url(r'^createReview', include('knowItAllAPI.createReview.urls')),
    url(r'^vote', include('knowItAllAPI.vote.urls')),

    url(r'^myPosts', include('knowItAllAPI.myPosts.urls')),
    url(r'^getPost', include('knowItAllAPI.getPost.urls')),
]