from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from progress.views import ProgressList
from user_profiles import views

urlpatterns = format_suffix_patterns([
        url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
        url(r'^users/(?P<user__username>[\w.@+-]+)/$', views.UserDetail.as_view(), name='username-detail'),
        url(r'^users/(?P<user__username>[\w.@+-]+)/progress/$', ProgressList.as_view(), name='username-progress'),
        url(r'users/$', views.UserCreate.as_view(), name='user-create'),
])

# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]