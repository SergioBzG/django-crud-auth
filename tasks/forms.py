from django.forms import ModelForm # This is a class that Django provides to create forms base in models
from .models import Task

class TaskForm(ModelForm):
    class Meta: # This class is used to specify the model that will be used to create the form
        model = Task
        fields = ['title', 'description', 'important']