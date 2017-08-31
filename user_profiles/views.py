from django.shortcuts import render
from django.contrib.auth.models import User
from user_profiles.models import Profile
from progress.models import Progress
from user_profiles.permissions import IsOwner
from user_profiles.serializers import ProfileSerializer, UserSerializer, UpdatePasswordSerializer
from rest_framework import generics, renderers, permissions, status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView
from django.views.generic.detail import DetailView

# Create your views here.


class UserCreate(generics.CreateAPIView):
    """
    Endpoint for user creation.
    """
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
    Endpoint for getting and updating user data using username as a lookup field
    """
    lookup_field = ('user__username')
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsOwner,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ChangePassword(APIView):
    """
    Endpoint for updating password.
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsOwner,)

    def get_object(self, value, queryset=None):
        return User.objects.get(username=value)

    def put(self, request, *args, **kwargs):
        self.object = self.get_object(kwargs.get('user__username'))
        serializer = UpdatePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Incorrect password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


