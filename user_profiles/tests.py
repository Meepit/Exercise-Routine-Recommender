from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    def create_user_data(self, *args, default=False, **kwargs):
        """
        Create user data.
        default=True will return valid user data
        """
        if default:
            return self.create_user_data(username="testuser",
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

    def test_create_user(self):
        """
        Test successful user creation with correct HTTP code (201 created)
        Test user successfully stored in database
        Test user password is hashed
        """
        url = reverse('user-create')
        data = self.create_user_data(default=True)
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
        data_no_username = self.create_user_data(password="")
        data_no_password = self.create_user_data(username="")
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
        data = self.create_user_data(default=True)
        data["is_superuser"] = True
        data["is_staff"] = True
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username="testuser").is_superuser, False)
        self.assertEqual(User.objects.get(username="testuser").is_staff, False)

