from rest_framework import serializers
from progress.models import Progress
from django.contrib.auth.models import User
from recommender.models import Exercise
from recommender.serializers import ExerciseSerializer


class ProgressSerializer(serializers.HyperlinkedModelSerializer):
    """
    exercise_id and exercise_name added as separate fields so that not as many GET requests
    needed in angular when generating visualisations.

    No need to add exercise_id and exercise_name to POST, they're generated from the exercise
    """
    #exercise = serializers.HyperlinkedIdentityField(many=False, view_name='exercise-detail', format='html', read_only=False)
    #exercise = ExerciseSerializer(many=False)
    exercise_id = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all(),source='exercise.id', required=False, allow_null=True)
    exercise_name = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all(),source='exercise.name', required=False, allow_null=True)
    #queryset=Exercise.objects.all(),

    class Meta:
        model = Progress
        fields = ('id', 'date', 'quantity', 'exercise', 'exercise_id', 'exercise_name', 'user')


