from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from progress import views

urlpatterns = format_suffix_patterns([
    url(r'^progress/$', views.ProgressList.as_view(), name='progress-list')
])

# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]