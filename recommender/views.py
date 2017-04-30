from recommender.models import Routine, Exercise, Workout
from recommender.serializers import ExerciseSerializer, WorkoutSerializer, RoutineSerializer
from rest_framework import generics, renderers
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Create your views here.


class RoutineList(generics.ListAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer


class RoutineDetail(generics.RetrieveAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer


class ExerciseList(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class ExerciseDetail(generics.RetrieveAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class WorkoutDetail(generics.RetrieveAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
