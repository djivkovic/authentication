from django.contrib import admin
from .models import User, GuideProfile, TouristProfile, AccountantProfile, AdministratorProfile, ModeratorProfile
# Register your models here.

admin.site.register(User)
admin.site.register(GuideProfile)
admin.site.register(TouristProfile)
admin.site.register(AccountantProfile)
admin.site.register(AdministratorProfile)
admin.site.register(ModeratorProfile)


