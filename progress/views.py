# Create your views here.
from progress.models import Progress
from progress.serializers import ProgressSerializer
from rest_framework import generics, renderers, permissions


class ProgressList(generics.ListCreateAPIView):
    serializer_class = ProgressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Filters Progress objects for objects linked to the user
        Admins can see all progress
        :return: filtered queryset
        """
        if self.request.user.is_superuser:
            queryset = Progress.objects.all()
        else:
            queryset = Progress.objects.filter(user__id=self.request.user.id)
        return queryset

    def perform_create(self, serializer):
        """
        Hook into create method to set user to currently logged in user.
        """
        serializer.save(user=self.request.user)


class ProgressDetail(generics.RetrieveAPIView):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
