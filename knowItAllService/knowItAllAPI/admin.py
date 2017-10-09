from django.contrib import admin
from .models import *

# Display tables on admin page
admin.site.register(UserProfile)
admin.site.register(Topic)
admin.site.register(Review)
admin.site.register(Poll)
admin.site.register(PollChoice)
admin.site.register(Vote)