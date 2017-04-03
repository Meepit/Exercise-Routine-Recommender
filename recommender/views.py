from django.shortcuts import render, redirect
from django.http import HttpResponse
from recommender.forms import RoutineForm
from django.template import Context, Template
from sklearn.externals import joblib

# Create your views here.


def make_classification(a_list):
    """
    Unchecked precondition: Classifier has not changed. If changed, gen new Classifier
    """
    routine_classifier = joblib.load('recommender/routine_classifier.pkl')
    result = routine_classifier.predict([a_list])
    return result[0]


def home(request):
    if request.method == 'POST':
        user_list = [request.POST["goal"], request.POST["equipment_use"],
                     request.POST["days_per_week"], request.POST["session_length"]]
        request.session['user_list'] = [int(i) for i in user_list]
        return redirect('/result')
    f = RoutineForm()
    return render(request, 'home.html', {'form': f.as_p()})


def result(request):
    if request.session['user_list']:
        user_list = request.session.pop('user_list', False)
        result = make_classification(user_list)
    return HttpResponse("Your recommmended routine is: %s" %result)
