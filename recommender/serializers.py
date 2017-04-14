from rest_framework import serializers
from recommender.models import Exercise, Workout, Routine


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'name', 'description', 'sets', 'reps')


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = ('id', 'name', 'description', 'exercises')


class RoutineSerializer(serializers.ModelSerializer):
    workout = WorkoutSerializer(many=True, read_only=True)

    class Meta:
        model = Routine
        fields = ('id', 'name', 'description', 'routine_type', 'equipment_needed',
                  'days_per_week', 'session_length', 'workout')

