"""routineapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

from ang.views import AngularTemplateView
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('recommender.urls')),
    url(r'^api/', include('progress.urls')),
    url(r'^api/', include('user_profiles.urls')),
    url(r'auth/token/$', obtain_jwt_token),  # Creates token on post for token based authentication
    url(r'^api/templates/(?P<item>[A-Za-z0-9\_\-\.\/]+)\.html$', AngularTemplateView.as_view()),

]

urlpatterns += [url(r'^', TemplateView.as_view(template_name='ang/index.html'))]  # Add angular index page

# Login and logout views for the browsable API
#urlpatterns += [
#    url(r'^api-auth/', include('rest_framework.urls',
#                               namespace='rest_framework')),
#]
