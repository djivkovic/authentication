from django.contrib import admin
from .models import User, GuideProfile, TouristProfile, AccountantProfile, AdministratorProfile, ModeratorProfile, HotelijerProfile, Reservation,Room
# Register your models here.

admin.site.register(User)
admin.site.register(GuideProfile)
admin.site.register(TouristProfile)
admin.site.register(AccountantProfile)
admin.site.register(AdministratorProfile)
admin.site.register(ModeratorProfile)
admin.site.register(HotelijerProfile)
admin.site.register(Reservation)
admin.site.register(Room)





