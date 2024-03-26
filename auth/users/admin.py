from django.contrib import admin
from .models import User, GuideProfile, TouristProfile
# Register your models here.

admin.site.register(User)
admin.site.register(GuideProfile)
admin.site.register(TouristProfile)
