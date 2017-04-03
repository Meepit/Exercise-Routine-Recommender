from django.core.management.base import BaseCommand, CommandError
from recommender.models import Routine
from sklearn import tree
from sklearn.externals import joblib
import pandas as pd

class Command(BaseCommand):
    help = 'Generates and saves a new tree Classifier, saves in recommender dir'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        '''
        Get all routines, store in Dataframe format.
        Train classifier and save.
        '''
        # Shape DataFrame
        routines = Routine.objects.all()
        names = [i.name for i in routines]
        routine_types = [i.routine_type for i in routines]
        equipment_needed = [i.equipment_needed for i in routines]
        days_per_weeks = [i.days_per_week for i in routines]
        session_lengths = [i.session_length for i in routines]
        routine_df = pd.DataFrame({
          'name': pd.Series(names),
          'type': pd.Series(routine_types),
          'equipment needed': pd.Series(equipment_needed),
          'days per week': pd.Series(days_per_weeks),
          'session length': pd.Series(session_lengths),
        })
        # Create classifier
        routine_df = routine_df[["name", "type", "equipment needed", "days per week", "session length"]]
        features = routine_df.columns[1:]
        target = routine_df["name"]
        routine_classifier = tree.DecisionTreeClassifier()
        routine_classifier.fit(routine_df[features], target)
        # Save classifier
        joblib.dump(routine_classifier, 'recommender/routine_classifier.pkl')
