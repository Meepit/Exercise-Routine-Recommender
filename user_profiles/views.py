from django.shortcuts import render
from django.contrib.auth.models import User
from user_profiles.models import Profile
from user_profiles.permissions import IsOwnerOrAdmin
from user_profiles.serializers import ProfileSerializer, UserSerializer
from rest_framework import generics, renderers, permissions

# Create your views here.


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @staticmethod
    def perform_create(serializer):
        """
        Always set added permissions to false.
        Staff and superusers should be created through admin page
        """
        serializer.save(is_staff=False, is_superuser=False)


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (IsOwnerOrAdmin,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


