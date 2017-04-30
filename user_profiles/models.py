from django.contrib.auth.models import User
from django.db import models
from recommender.models import Routine
from progress.models import Progress

# Create your models here.


class Profile(models.Model):
    """
    Profile is just an extension table of User, allowing us to add additional fields. They both have 1 to 1 relationships.
    In this case Profile is currently just being used to link a routine. This is preferred method from django docs.
    """
    user = models.OneToOneField(User)
    routine = models.ForeignKey(Routine, blank=True, null=True)

    def __str__(self):
        return self.user.username + " Profile"

    @property
    def get_progress(self):
        """Return progress objects belonging to user.
            Set as property to allow serializer to add progress"""
        progress = Progress.objects.all().filter(user__id=self.user.id)
        return progress

