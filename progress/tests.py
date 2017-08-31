from django.urls import reverse
import json
from recommender.models import Exercise
from progress.models import Progress
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from recommender.models import Routine
from user_profiles.models import Profile
from user_profiles.tests import create_user_data
from recommender.tests import create_routines
from django.contrib.auth.models import User
from progress.views import ProgressList
from rest_framework.test import APIRequestFactory, force_authenticate


class ProgressTests(APITestCase):
    def create_test_user_and_routine(self):
        """
        Create a user
        Assign Starting Strength routine to the user's profile
        """
        # Create user
        data = create_user_data(default=True)
        url = reverse('user-create')
        self.client.post(url, data, format='json')
        # Create and assign routine
        create_routines()
        profile = Profile.objects.get(user__id=1)
        profile.routine = Routine.objects.get(pk=1)

    def test_post_progress(self):
        """
        Test that progress can be posted and is successfully displayed on a user's profile
        """
        self.create_test_user_and_routine()
        data = {
            "quantity": 33,
            "exercise": reverse('exercise-detail', args=[1]),
            "user": reverse('user-detail', args=[1])
        }
        factory = APIRequestFactory()
        view = ProgressList.as_view()
        request = factory.post('/api/progress/', data)
        force_authenticate(request, user=User.objects.get(pk=1))
        response = view(request).render()
        response_content = response.content.decode('utf8')
        response_content = json.loads(response_content)
        self.assertEqual(response_content["user"], "http://testserver" + reverse('user-create')+"1/")
        self.assertEqual(response_content["exercise"], "http://testserver/api/exercises/1/")
        # Create 2nd user and assert they cannot see unrelated progress
        User.objects.create(username="secondtestuser", password="testpassword2")
        second_user = User.objects.get(username="secondtestuser")
        second_user.routine=Routine.objects.get(pk=1)
        view = ProgressList.as_view()
        request = factory.get('/api/progress/')
        force_authenticate(request, user=User.objects.get(pk=2))
        response = view(request).render()
        response_content = response.content.decode('utf8')
        response_content = json.loads(response_content)
        self.assertEqual(response_content, [])

    def test_authentication(self):
        response = self.client.get(reverse('progress-list'))
        response_content = response.content.decode('utf8')
        response_content = json.loads(response_content)
        self.assertEqual(response_content["detail"], "Authentication credentials were not provided.")

    def test_progress_validation(self):
        self.create_test_user_and_routine()
        data = {
            "quantity": "abc",
            "exercise": reverse('exercise-detail', args=[1]),
            "user": reverse('user-detail', args=[1])
        }
        factory = APIRequestFactory()
        view = ProgressList.as_view()
        request = factory.post('/api/progress/', data)
        force_authenticate(request, user=User.objects.get(pk=1))
        response = view(request).render()
        response_content = response.content.decode('utf8')
        self.assertIn("integer is required", response_content)
