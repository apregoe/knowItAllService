from django.contrib import admin
from .models import *

# Display tables on admin page
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Review)
admin.site.register(Poll)
admin.site.register(PollChoice)
admin.site.register(Notification)
admin.site.register(Vote)
admin.site.register(Tag)
admin.site.register(TagLinker)
admin.site.register(Comment)
admin.site.register(Opinion)