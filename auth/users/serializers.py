from rest_framework import serializers
from .models import User, GuideProfile, TouristProfile, AdministratorProfile, AccountantProfile, ModeratorProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'user_type']  
        extra_kwargs = {
            'password': {'write_only': True},
            'user_type': {'required': True}  
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_type = validated_data.get('user_type')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        # Create profile based on user type
        if user_type == User.TOURIST:
            TouristProfile.objects.create(user=instance)
        elif user_type == User.GUIDE:
            GuideProfile.objects.create(user=instance)
        elif user_type == User.ADMINISTRATOR:
            AdministratorProfile.objects.create(user=instance)
        elif user_type == User.ACCOUNTANT:
            AccountantProfile.objects.create(user=instance)
        elif user_type == User.MODERATOR:
            ModeratorProfile.objects.create(user=instance)

        return instance
