from django.shortcuts import render, redirect
from django.http import HttpResponse
from recommender.forms import RoutineForm
from django.template import Context, Template
from sklearn.externals import joblib

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


class ExerciseList(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer()


class WorkoutList(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = WorkoutSerializer()



