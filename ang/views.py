import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.generic import View

from django.shortcuts import render


class AngularTemplateView(View):
    """
    Load angular
    """
    def get(self, request, item=None, *args, **kwargs):
        template = settings.TEMPLATES[0]["DIRS"][0]
        path = os.path.join(template, "ang", item + ".html")
        try:
            html = open(path)
            return HttpResponse(html)
        except:
            raise Http404
