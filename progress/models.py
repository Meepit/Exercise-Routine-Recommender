from datetime import date
from django.contrib.auth.models import User
from django.db import models
from recommender.models import Exercise

# Create your models here.


class Progress(models.Model):
    """
    Progress refers to the progress a user makes for a single exercise
    Progress records will be recorded against a single exercise and a single user.
    Quantity in the vast majority of cases refers to weight, but can refer to other things such as number of pullups
    """
    date = models.DateField(default=date.today)
    quantity = models.IntegerField()
    User = models.ForeignKey(User)
    Exercise = models.ForeignKey(Exercise)

    def __str__(self):
        return self.User.name + " " + self.Exercise.name.split("x")[0][:-2] + " " + self.date



