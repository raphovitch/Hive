from django.contrib import admin
from first_app.models import Tweet, UserProfileInfo

# Register your models here.
admin.site.register(Tweet)
admin.site.register(UserProfileInfo)