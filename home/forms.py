from .models import models
from django import forms

class ModelsForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields - "__all__"