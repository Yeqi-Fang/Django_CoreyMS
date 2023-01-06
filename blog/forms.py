from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment


class CommetForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
