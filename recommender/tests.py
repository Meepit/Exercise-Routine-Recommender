from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from django.contrib.auth.models import User
import json
from user_profiles.models import Profile
from user_profiles.views import UserDetail
from recommender.models import Routine, Exercise, Workout


def create_user_data(*args, default=False, **kwargs):
    """
    Create user data.
    default=True will return valid user data
    """
    if default:
        return create_user_data(username="testuser",
                                password="thisisatestpw",
                                first_name="testname",
                                email="testemail@testmail.co.za")
    data = {
        "username": "",
        "password": "",
        "first_name": "",
        "email": ""
    }
    for i in kwargs.keys():
        if i in data.keys():
            data[i] = kwargs[i]
    return data


def create_routines():
    """
    Creates a Routine entry
    NOTE: In Django an object making use of a many to many relationship needs to be saved before the relationship is added
    """
    Exercise(name="benchpress 5x5", sets=5, reps=5).save()
    Exercise(name="squat 5x5", sets=5, reps=5).save()
    Exercise(name="deadlift 1x5", sets=1, reps=5).save()
    workout1 = Workout(name="starting strength a")
    workout1.save()
    workout1.exercises.add(Exercise.objects.get(pk=1), Exercise.objects.get(pk=2))
    workout2 = Workout(name="starting strength b")
    workout2.save()
    workout2.exercises.add(Exercise.objects.get(pk=2), Exercise.objects.get(pk=3))
    routine1 = Routine(name="starting strength", routine_type=1, equipment_needed=0, days_per_week=3, session_length=76)
    routine1.save()
    routine1.workout.add(Workout.objects.get(pk=1), Workout.objects.get(pk=2))
    return routine1



"""Classification tests run outside test environment"""
