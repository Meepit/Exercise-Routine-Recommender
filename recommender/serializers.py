from rest_framework import serializers
from recommender.models import Exercise, Workout, Routine


class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'name', 'description', 'sets', 'reps')


class WorkoutSerializer(serializers.HyperlinkedModelSerializer):
    #exercises = ExerciseSerializer(many=True, read_only=True)
    exercises = serializers.HyperlinkedIdentityField(many=True, view_name='exercise-detail', format='html')

    class Meta:
        model = Workout
        fields = ('id', 'name', 'description', 'exercises')


class RoutineSerializer(serializers.HyperlinkedModelSerializer):
    #workout = WorkoutSerializer(many=True, read_only=True)
    workout = serializers.HyperlinkedIdentityField(many=True, view_name='workout-detail', format='html')

    class Meta:
        model = Routine
        fields = ('id', 'name', 'description', 'routine_type', 'equipment_needed',
                  'days_per_week', 'session_length', 'workout')

