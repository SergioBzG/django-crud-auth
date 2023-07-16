from django import forms # This is a class that Django provides to create forms
from .models import Task

class TaskForm(forms.ModelForm):
    # ModelForm is a class that Django provides to create forms base in models
    class Meta: # This class is used to specify the model that will be used to create the form
        model = Task
        fields = ['title', 'description', 'important']
        # widgets attribute is used to customize the form fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }