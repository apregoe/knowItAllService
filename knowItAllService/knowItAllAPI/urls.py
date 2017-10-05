from django.conf.urls import url, include
from . import views
# . means importing from current directory

urlpatterns = [
    url(r'^$', views.index, name='index'), # This is the base index for .../api/
    # url(r'^register/', include('register.urls')), # This is .../api/register
    url(r'^createPost/', include('knowItAllAPI.createPost.urls')),  # This is .../api/createPost
]
