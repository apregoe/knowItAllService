from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.createTopic), # This is the base index for .../api/
]