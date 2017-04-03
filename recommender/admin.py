from django.contrib import admin
from .models import Routine, Workout, Exercise
# Register your models here.
admin.site.register(Routine)
admin.site.register(Workout)
admin.site.register(Exercise)

