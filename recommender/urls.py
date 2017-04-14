from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from recommender import views

urlpatterns = format_suffix_patterns([
    url(r'^routines/$', views.RoutineList.as_view(), name='routine-list')
])

