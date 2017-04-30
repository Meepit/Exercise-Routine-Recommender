from rest_framework import serializers
from progress.models import Progress
from django.contrib.auth.models import User
from recommender.models import Exercise
from recommender.serializers import ExerciseSerializer


class ProgressSerializer(serializers.HyperlinkedModelSerializer):
    # Exercise = ExerciseSerializer(many=True, read_only=True)
    class Meta:
        model = Progress
        fields = ('id', 'date', 'quantity', 'exercise', 'user')


