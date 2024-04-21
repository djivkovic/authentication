from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, user_type=None):
        if not email:
            raise ValueError('Email address is required')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, user_type=user_type)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email=email, name=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin): 
    GUIDE = 'Guide'
    TOURIST = 'Tourist'
    ADMINISTRATOR = 'Administrator'
    ACCOUNTANT = 'Accountant'
    MODERATOR = 'Moderator'
    HOTELIJER = 'Hotelijer'
    UNAUTHENTICATED = 'UNA'
    
    USER_TYPE_CHOICES = [
        (GUIDE, 'Guide'),
        (TOURIST, 'Tourist'),
        (ADMINISTRATOR, 'Administrator'),
        (ACCOUNTANT, 'Accountant'),
        (MODERATOR, 'Moderator'),
        (HOTELIJER, 'Hotelijer'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=UNAUTHENTICATED)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):  
        return self.is_staff




class Room(models.Model):
    id = models.AutoField(primary_key=True)
    room_number = models.DecimalField(max_digits=10, decimal_places=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Soba {self.room_number} - Cena: {self.price} - Zauzeta: {self.is_booked}"

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_booked = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Rezervacija sobe {self.room.room_number} - Datum rezervacije: {self.date_booked}"
    
class GuideProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guide_profile')
    bio = models.TextField()
    ture = models.CharField(max_length=100)  

class TouristProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tourist_profile')
    turista = models.CharField(max_length=100)  
    
class AdministratorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='administrator_profile')
    administrator = models.CharField(max_length=100)  
    
class AccountantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='accountant_profile')
    accountant = models.CharField(max_length=100)  
    
class ModeratorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='moderator_profile')
    moderator = models.CharField(max_length=100)  
    
class HotelijerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hotelijer_profile')
    hotelijer = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Profil hotela '{self.hotelijer}, Balance: {self.balance} , Room: {self.room}'"