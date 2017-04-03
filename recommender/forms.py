from django import forms

class RoutineForm(forms.Form):
    goal = forms.ChoiceField([
            (1, "Hypertrophy"),
            (0,"Strength")])

    equipment_use = forms.ChoiceField([
            (0,"Minimal (Barbell)"),
            (1,"Variety"),])
    days_per_week = forms.ChoiceField([(1,1),(2,2),(3,3),(4,4),(5,5)])
    session_length = forms.ChoiceField([(45,45),(60,60),(75,75),(90,90),(120,120)
    ])
