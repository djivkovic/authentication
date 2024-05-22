from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from enum import Enum

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
    hotelijer = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 

    def __str__(self):
        return f"Soba {self.room_number} - Cena: {self.price} - Zauzeta: {self.is_booked} {self.hotelijer}"

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_booked = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Rezervacija sobe {self.room.room_number} - Datum rezervacije: {self.date_booked}"
    
class Contract(models.Model):
    class Status(Enum):
        PENDING = 'pending'
        REJECTED = 'rejected'
        ACCEPTED = 'accepted'

    contractId = models.AutoField(primary_key=True)
    hotelijerId = models.IntegerField()
    hotelijerName = models.CharField(max_length=100)
    hotelijerMessage = models.CharField(max_length=1000)
    withdrawCondition = models.CharField(max_length=1000)
    percentage = models.DecimalField(max_digits=3, decimal_places=0)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[(status.value, status.name) for status in Status], default="pending")

    def __str__(self):
        return f"Contract {self.contractId} - Hotelijer: {self.hotelijerName}, Status: {self.status}"
    
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
    hotelijer = models.CharField(max_length=100, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rooms = models.ManyToManyField(Room, related_name='hotelijeri', null=True)
    percentage = models.IntegerField(default=0)

    def __str__(self):
        return f"Profil hotela '{self.hotelijer}', Balance: {self.balance}, Rooms: {self.rooms.all()}, Percentage: {self.percentage}%"

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    userId = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    hotelijer_profile = models.ForeignKey(HotelijerProfile, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.id} - Amount: {self.amount}, User ID: {self.userId}, Created At: {self.created_at}"

    def save(self, *args, **kwargs):
        if self._state.adding and self.hotelijer_profile:
            self.hotelijer_profile.balance += self.amount
            self.hotelijer_profile.save()

        super(Transaction, self).save(*args, **kwargs)