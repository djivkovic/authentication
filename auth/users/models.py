from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin): 
    GUIDE = 'Guide'
    TOURIST = 'Tourist'
    ADMINISTRATOR = 'Administrator'
    ACCOUNTANT = 'Accountant'
    MODERATOR = 'Moderator'
    UNAUTHENTICATED = 'UNA'
    
    USER_TYPE_CHOICES = [
        (GUIDE, 'Guide'),
        (TOURIST, 'Tourist'),
        (ADMINISTRATOR, 'Administrator'),
        (ACCOUNTANT, 'Accountant'),
        (MODERATOR, 'Moderator'),
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


class GuideProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guide_profile')
    bio = models.TextField()
    ture = models.CharField(max_length=100)  

class TouristProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tourist_profile')
    turista = models.CharField(max_length=100)  