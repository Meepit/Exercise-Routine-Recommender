from django.urls import reverse
from django.contrib.auth.models import User
import json
from recommender.tests import create_routines
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


class UserTests(APITestCase):
    """
    Note: Response must be rendered to get content,
          Status codes can be retrieved without rendering.
    """

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

    def test_password_validation_length(self):
        """
        Test user is not created when a password of insufficient length is supplied
        """
        url = reverse('user-create')
        data = create_user_data(username="testusername", password="123", first_name="Jim", email="jimjones@jim.com")
        response = self.client.post(url, data, format='json')
        self.assertIn("too short", response.render().content.decode('utf8'))

    def test_password_validation_chars(self):
        """
        Test user is not created when a password containing disallowed characters is supplied
        """
        url = reverse('user-create')
        data = create_user_data(username='testerme', password="passwor<>;345", first_name="John", email="email33@t.com")
        response = self.client.post(url, data, format='json')
        self.assertIn("Cannot contain", response.render().content.decode('utf8'))

    def test_password_validation_length_chars(self):
        """
        Test user is not created and appropriate errors are returned when a password of insufficient length and
         containing diallowed characters is supplied.
        """
        url = reverse('user-create')
        data = create_user_data(username='testa', password="[];", first_name="Jimbo", email="alskjd@alskd.com")
        response = self.client.post(url, data, foramt='json')
        response_content = response.render().content.decode('utf8')
        self.assertIn("Cannot contain", response_content)
        self.assertIn("too short", response_content)

    def test_unique_email(self):
        """
        Test only a single user can be created with a given email.
        """
        url = reverse('user-create')
        valid_data = create_user_data(username='test1', password="validpassword", first_name="valid", email="lk@kj.com")
        invalid_data = create_user_data(username='test2', password="validpwaaa", first_name="valid", email="lk@kj.com")
        response = self.client.post(url, valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, invalid_data, format='json')
        self.assertIn("be unique", response.render().content.decode('utf8'))

    def test_email_validation_chars(self):
        """
        Test account is not created if disallowed characters are supplied
        """
        url = reverse('user-create')
        data = create_user_data(username='tst1', password='validpasswrd', first_name='valid', email=';></@gm.com')
        response = self.client.post(url, data, format='json')
        self.assertIn("Cannot contain", response.render().content.decode('utf8'))

    def test_username_validation_chars(self):
        """
        Test account is not created if disallowed characters are supplied
        """
        url = reverse('user-create')
        data = create_user_data(username='<>/;', password='validpasswrd', first_name='valid', email='test@test.com')
        response = self.client.post(url, data, format='json')
        self.assertIn("Cannot contain", response.render().content.decode('utf8'))

    def test_name_validation_chars(self):
        """
        Test account is not created if disallowed characters are supplied
        """
        url = reverse('user-create')
        data = create_user_data(username='asdga', password='validpasswrd', first_name=']><#', email='test@test.com')
        response = self.client.post(url, data, format='json')
        self.assertIn("Cannot contain", response.render().content.decode('utf8'))



class ProfileTests(APITestCase):
    """
    force_authenticate forces authenticate, not sure if able to integrate JWT authentication with django tests.
    """

    def test_successful_profile_creation(self):
        """"
        Test that profiles are successfully automatically constructed on User creation.
        """
        data = create_user_data(default=True)
        url = reverse('user-create')
        self.client.post(url, data, format='json')
        factory = APIRequestFactory()
        user = User.objects.get(username=data["username"])
        view = UserDetail.as_view()
        # Authenticate
        request = factory.get('/api/users')
        force_authenticate(request, user=user)
        response = view(request, user__username=data["username"])
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
        response = self.client.get('/api/users/testuser/')
        self.assertIn('Not found', response.content.decode('utf8'))

    def test_permissions(self):
        """
        Test authenticated users only have access to their own data
        """
        data_user_1 = create_user_data(username="user1",
                                       first_name="myfirstname",
                                       password="testpassword",
                                       email="testemail@test.com")
        data_user_2 = create_user_data(username="user2",
                                       first_name="John",
                                       password="testpassword22",
                                       email="test@tas.com")
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
        response = view(request, user__username=data_user_2["username"])
        response_content = response.render().content.decode('utf8')
        response_content = json.loads(response_content)
        self.assertIn("You do not have permission", response_content["detail"])

    def test_change_password(self):
        """
        Test successful password change
        """
        url = reverse('user-create')
        data = create_user_data(default=True)
        self.client.post(url, data, format='json')
        old_password = User.objects.get(username=data["username"]).password
        pw_data = {'old_password': data["password"], 'new_password': "newpassword123"}
        request = self.client.put('/api/users/testuser/changepassword/', pw_data, format='json')
        user = User.objects.get(username=data["username"])
        force_authenticate(request, user=user)
        new_password = User.objects.get(username=data["username"]).password
        self.assertNotEqual(old_password, new_password)

    def test_change_password_wrong_old_password(self):
        """
        Test password is not changed when incorrect old password is supplied
        """
        url = reverse('user-create')
        data = create_user_data(default=True)
        self.client.post(url, data, format='json')
        old_password = User.objects.get(username=data["username"]).password
        pw_data = {'old_password': 'incorrect', 'new_password': 'newpassword123'}
        response = self.client.put('/api/users/testuser/changepassword/', pw_data, format='json')
        user = User.objects.get(username=data["username"])
        force_authenticate(response, user=user)
        self.assertIn('Incorrect', response.render().content.decode('utf8'))
        new_password = User.objects.get(username=data["username"]).password
        self.assertEqual(old_password, new_password)

    def test_password_validation_new_password(self):
        """
        Test proper validation is done on new password
        """
        url = reverse('user-create')
        data = create_user_data(default=True)
        self.client.post(url, data, format='json')
        old_password = User.objects.get(username=data["username"]).password
        pw_data = {'old_password': data["password"], 'new_password': '?;;><>'}
        response = self.client.put('/api/users/testuser/changepassword/', pw_data, format='json')
        user = User.objects.get(username=data["username"])
        force_authenticate(response, user=user)
        new_password = User.objects.get(username=data["username"]).password
        response_content = response.render().content.decode('utf8')
        self.assertIn('too short', response_content)
        self.assertIn('Cannot contain', response_content)
        self.assertEqual(old_password, new_password)

    def test_routine_change(self):
        """
        Test routine can be updated with PUT request
        """
        # Create user, routine
        create_routines()
        url = reverse('user-create')
        user_data = create_user_data(default=True)
        self.client.post(url, user_data, format='json')
        # Change routine
        factory = APIRequestFactory()
        data = {'routine_id': "1"}
        view = UserDetail.as_view()
        user = User.objects.get(username=user_data["username"])
        request = factory.put('/api/users/%s' % user_data["username"], data)
        force_authenticate(request, user=user)
        response = view(request, user__username=user_data["username"])
        self.assertIn("starting strength", response.render().content.decode('utf8'))



