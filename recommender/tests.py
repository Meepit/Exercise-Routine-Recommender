from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from user_profiles.tests import create_user_data
from django.contrib.auth.models import User
import json
from user_profiles.models import Profile
from user_profiles.views import UserDetail
from recommender.models import Routine, Exercise, Workout


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


class RoutineTests(APITestCase):
    def test_routine_assignment(self):
        """
        Test that routine objects can be successfully created and assigned to user profiles
        Test that profile serializer correctly displays
        """
        create_routines()
        data = create_user_data(default=True)
        url = reverse('user-create')
        self.client.post(url, data, format='json')
        profile = Profile.objects.get(user__id=1)
        self.assertEqual(profile.routine, None)
        #self.client.patch(reverse('user-detail'), {"routine": Routine.objects.get(pk=1)}, format='json')
        profile.routine = Routine.objects.get(pk=1)
        profile.save()
        self.assertEqual(profile.routine, Routine.objects.get(pk=1))
        factory = APIRequestFactory()
        user = User.objects.get(username=data["username"])
        view = UserDetail.as_view()
        request = factory.get('/api/users')
        force_authenticate(request, user=user)
        response = view(request, pk=user.pk)
        response_content = response.render().content.decode('utf8')
        response_content = json.loads(response_content)
        self.assertEqual(response_content["routine"], "http://testserver/api/routines/1/")

"""Classification tests run outside test environment"""





