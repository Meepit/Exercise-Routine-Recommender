from django.shortcuts import render
from django.contrib.auth.models import User
from user_profiles.models import Profile
from progress.models import Progress
from user_profiles.permissions import IsOwnerOrAdmin
from user_profiles.serializers import ProfileSerializer, UserSerializer
from rest_framework import generics, renderers, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.views.generic.detail import DetailView

# Create your views here.


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @staticmethod
    def perform_create(serializer):
        """
        Always set added permissions to false.
        Staff and superusers should be created through admin page
        """
        serializer.save(is_staff=False, is_superuser=False)
        # Get saved user and create profile
        created_user = User.objects.get(username=dict(serializer.data)["username"])
        Profile.objects.create(user=created_user)


class UserDetail(generics.RetrieveUpdateAPIView):
    """
    Performs lookup using User.username. Need to be able to lookup by username
    for token based authentication.
    """
    lookup_field = ('user__username')
    permission_classes = (IsOwnerOrAdmin,)
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
