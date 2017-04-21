from django.test import TestCase
from django.contrib.auth.models import User
from progress.views import ProgressList
from rest_framework.test import APIRequestFactory, force_authenticate

factory = APIRequestFactory()
user = User.objects.get(username='test1')
view = ProgressList.as_view()

request = factory.get('/progress/')
force_authenticate(request, user=user)
response = view(request)
