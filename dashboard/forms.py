from django import forms

from dashboard.models import *


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']


class DateInput(forms.DateInput):
    input_type = 'date'


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        widgets = {'due': DateInput()}
        fields = '__all__'
