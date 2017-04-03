from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.db import models
import os
import pandas as pd
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from recommender.choices import *
# Create your models here.
'''
Tables: Workout, Routine, Exercise
'''


class Exercise(models.Model):
    """
    An exercise refers to each individual exercise to be performed in a workout.
    An exercise has sets which refers to how many times it should be performed per workout
    An exercise has reps which refers to how many repititions it should be performed per set

    For the purpose of this project, several of the same exercise can exist if 2 or more instances have different sets
    or reps. I.E "Benchpress" in workoutA may need to be performed for 3 sets and 10 reps. Whereas in workoutB it may
    need to be performed for 5 sets and 5 reps. This will result in 2 separate entries.

    Naming convention: Exercise name lowercase followed by no. sets followed by x followed by no. reps
                      I.E squat 5x5, benchpress 3x10
    """

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True)
    sets = models.IntegerField()
    reps = models.IntegerField()

    def __str__(self):
        return self.name


class Workout(models.Model):
    """
    A 'Workout' refers to a group of exercises to be performed on a particular day of a Routine. The set of exercises
    in a workout will be a subset of the complete set of exercises in a routine. Typically a routine will have anywhere
    from 2-5 different workouts.

    Naming conventions: lower case routine name, followed by incrementing alphabetical letters.
                       I.E starting strength a, starting strength b, starting strength c etc
    """
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True)
    exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return self.name


class Routine(models.Model):
    """
    Routine refers to a predefined set of exercises to be perfomed a predefined set of times per week.
    The Routine table is what the decision tree classifier will use to recommend routines, additionally it contains
    a reference to the Workout table which allows for tracking logical groupings of exercises related to a routine.

    equipment_needed and routine_type are mapped to integer fields to facilitate the DTC, however the admin panel
    will still display string fields to reduce confusion when adding / editing.

    Naming convention: lowercase I.E starting strength, westside for beginners etc
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    routine_type = models.IntegerField(choices=ROUTINE_TYPE_CHOICES)
    equipment_needed = models.IntegerField(choices=EQUIPMENT_CHOICES)
    days_per_week = models.IntegerField()
    session_length = models.IntegerField()
    workout = models.ManyToManyField(Workout)

    valid_classifiers = ["tree", "forest"]

    def __str__(self):
        return self.name

    @staticmethod
    def generate_classifier(prioritize=(), classifier_type="tree"):
        """
        prioritize = 2ary tuple (priority column, priority value)
        classifier_type = A valid classifier
        Preconditions: classifier_type must be Tree or Forest, prioritize must be a valid class variable
        Postconditions: If no existing classifier matching given parameters exists, a new classifier will be created.
                       If an existing classifier matching given parameters exists, nothing will be done.
        Return: filename of created classifier (not file path)
        TODO: Handle case where 0 records returned (I.E session_length__lte=30)
        """
        if type(prioritize) != tuple or type(classifier_type) != str or type(prioritize[1]) != int:
            raise TypeError("classifier_type accepts strings, prioritize bust be 2ary-tuple with an int for 2nd value")

        filename = classifier_type + "_" + prioritize[0].lower() + '_' + (str(prioritize[1]) if prioritize[0]
                                  not in ["days_per_week", "session_length"] else 'lte_' + str(prioritize[1])) + '.pkl'
        existing_classifiers = [file for file in os.listdir("recommender/classifiers")]
        if filename in existing_classifiers:
            # Exit function, tree exists
            print("{0} already exists.".format(filename))
            return filename
        # Build query
        routines = Routine.objects.all()
        if prioritize[0].lower() == "routine_type":
            routines = routines.filter(routine_type=prioritize[1])
        elif prioritize[0].lower() == "equipment_needed":
            routines = routines.filter(equipment_needed=0)  # Will only ever need to filter for "basic"
        elif prioritize[0].lower() == "days_per_week":
            routines = routines.filter(days_per_week__lte=prioritize[1])  # Not necessary to filter for gte
        elif prioritize[0].lower() == "session_length":
            routines = routines.filter(session_length__lte=prioritize[1])

        assert len(routines) > 0

        # Shape DataFrame
        routine_df = pd.DataFrame({
          'name': pd.Series([i.name for i in routines]),
          'type': pd.Series(i.routine_type for i in routines),
          'equipment needed': pd.Series(i.equipment_needed for i in routines),
          'days per week': pd.Series(i.days_per_week for i in routines),
          'session length': pd.Series(i.session_length for i in routines),
        })
        # Create classifier
        routine_df = routine_df[["name", "type", "equipment needed", "days per week", "session length"]]
        features = routine_df.columns[1:]
        target = routine_df["name"]
        routine_classifier = tree.DecisionTreeClassifier()
        if classifier_type.lower() == "forest":
            routine_classifier = RandomForestClassifier(n_estimators=10)
        routine_classifier.fit(routine_df[features], target)

        # Save classifier, use named identifier
        joblib.dump(routine_classifier, 'recommender/classifiers/' + filename)
        print("Created new {0} classifier named {1}".format(classifier_type, filename))
        if classifier_type.lower() == "tree":
            tree.export_graphviz(routine_classifier)
            print("Created visualization")
        return filename

    def save(self, *args, **kwargs):
        """
        Delete all existing classifiers
        """
        for file in os.scandir("recommender/classifiers"):
            if file.name.endswith(".pkl"):
                os.unlink(file.path)
        super(Routine, self).save(*args, **kwargs)


@receiver(pre_delete, sender=Routine)
# @receiver is a subscriber that is called before a Routine entry is deleted
# Overriding .save() only works when a single entry is deleted and not on bulk deletes.
def delete_existing_classifiers(sender, **kwargs):
    for file in os.scandir("recommender/classifiers"):
        if file.name.endswith(".pkl"):
            os.unlink(file.path)
