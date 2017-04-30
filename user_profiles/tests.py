from django.urls import reverse
from django.contrib.auth.models import User
import json
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from rest_framework import status
from user_profiles.views import UserDetail


def create_user_data(*args, default=False, **kwargs):
    """
    Create user data.
    default=True will return valid user data
    """
    if default:
        return create_user_data(username="testuser",
                                password="testpw",
                                first_name="testname",
                                last_name="testlastname",
                                email="testemail@testmail.co.za")
    data = {
        "username": "",
        "password": "",
        "first_name": "",
        "last_name": "",
        "email": ""
    }
    for i in kwargs.keys():
        if i in data.keys():
            data[i] = kwargs[i]
    return data


class UserTests(APITestCase):
    def test_create_user(self):
        """
        Test successful user creation with correct HTTP code (201 created)
        Test user successfully stored in database
        Test user password is hashed
        """
        url = reverse('user-create')
        data = create_user_data(default=True)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertNotEqual(User.objects.get().password, 'testpw')

    def test_bad_user_creation(self):
        """
        Test unsuccessful user creation due to blank username or password field
        Test that 201 status code is not returned
        Test that user count in database has not incremented
        """
        url = reverse('user-create')
        data_no_username = create_user_data(password="")
        data_no_password = create_user_data(username="")
        num_users = User.objects.count()
        response = self.client.post(url, data_no_username, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, data_no_password, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), num_users)

    def test_no_added_params(self):
        """
        Test that added User creation parameters cannot be set on creation.
        is_superuser and is_staff should always default to False
        """
        url = reverse('user-create')
        data = create_user_data(default=True)
        data["is_superuser"] = True
        data["is_staff"] = True
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username="testuser").is_superuser, False)
        self.assertEqual(User.objects.get(username="testuser").is_staff, False)


class ProfileTests(APITestCase):
    def test_successful_profile_creation(self):
        """"
        Test that profiles are successfully automatically constructed on User creation.
        """
        data = create_user_data(default=True)
        url = reverse('user-create')
        self.client.post(url, data, format='json')
        user_id = User.objects.get(username=data["username"]).pk
        factory = APIRequestFactory()
        user = User.objects.get(username=data["username"])
        view = UserDetail.as_view()
        # Authenticate
        request = factory.get('/api/users')
        force_authenticate(request, user=user)
        response = view(request, pk=user_id)
        response_content = response.render().content.decode('utf8')
        response_content = json.loads(response_content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_content["user"]["username"], data["username"])
        self.assertEqual(response_content["routine"], None)

    def test_no_profile_on_bad_creation(self):
        """
        Test that a profile is not created if User creation fails.
        """
        data = create_user_data()
        url = reverse('user-create')
        self.client.post(url, data, format='json')
        response = self.client.get('/api/users/1')
        self.assertEqual(response.content.decode('utf8'), '')

    def test_permissions(self):
        """
        Test authenticated users only have access to their own data
        """
        data_user_1 = create_user_data(username="user1", password="testpassword")
        data_user_2 = create_user_data(username="user2", password="testpassword22")
        url = reverse('user-create')
        self.client.post(url, data_user_1, format='json')
        self.client.post(url, data_user_2, format='json')
        user1 = User.objects.get(username="user1")
        user2 = User.objects.get(username="user2")
        factory = APIRequestFactory()
        view = UserDetail.as_view()
        # Authenticate as user 1 and try to view user2 profile data
        request = factory.get('/api/users/%s' % user1.pk)
        force_authenticate(request, user=user1)
        response = view(request, pk=user2.pk)
        response_content = response.render().content.decode('utf8')
        response_content = json.loads(response_content)
        self.assertIn("You do not have permission", response_content["detail"])