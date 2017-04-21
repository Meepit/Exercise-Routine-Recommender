from user_profiles.models import Profile
from rest_framework import serializers
from progress.serializers import ProgressSerializer
from recommender.serializers import RoutineSerializer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        # extra_kwargs allows for additional write fields that wont be displayed views
        extra_kwargs = {
            'password': {
                'write_only': True}
        }

    def create(self, validated_data):
        """ Overwrite create method to allow for password hashing on creation"""
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    routine = RoutineSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)
    progress = ProgressSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'routine', 'progress')
