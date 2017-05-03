from recommender.models import Routine, Exercise, Workout
from recommender.serializers import ExerciseSerializer, WorkoutSerializer, RoutineSerializer
from rest_framework import generics, renderers, views
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from sklearn.externals import joblib
# Create your views here.


class RoutineList(generics.ListAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer


class RoutineDetail(generics.RetrieveAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer


class ExerciseList(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class ExerciseDetail(generics.RetrieveAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class WorkoutDetail(generics.RetrieveAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer


class MakeClassification(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        post_dict = {
            "routine_type": request.data.get('routine_type', None),
            "equipment_needed": request.data.get('equipment_needed', None),
            "days_per_week": request.data.get('days_per_week', None),
            "session_length": request.data.get('session_length', None),
            "priority_field": request.data.get('priority_field', None),
        }
        if None in post_dict.values():
            return Response({"Routine": "There was a problem getting a routine."})
        else:
            clf_name = Routine.generate_classifier(prioritize=(post_dict["priority_field"], post_dict[post_dict["priority_field"]]))
            classifier = joblib.load('recommender/classifiers/'+clf_name)
            suggested_routine = classifier.predict([[post_dict["routine_type"],
                                                     post_dict["equipment_needed"],
                                                     post_dict["days_per_week"],
                                                     post_dict["session_length"]]])
            return Response({"Success": suggested_routine})


