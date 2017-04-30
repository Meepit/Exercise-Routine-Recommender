from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from recommender import views

urlpatterns = format_suffix_patterns([
    url(r'^routines/$', views.RoutineList.as_view(), name='routine-list'),
    url(r'routines/(?P<pk>[0-9]+)/$', views.RoutineDetail.as_view(), name='routine-detail'),
    url(r'^exercises/$', views.ExerciseList.as_view(), name='exercise-list'),
    url(r'exercises/(?P<pk>[0-9]+)/$', views.ExerciseDetail.as_view(), name='exercise-detail'),
    url(r'workouts/(?P<pk>[0-9]+)/$', views.WorkoutDetail.as_view(), name='workout-detail'),

])

# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]