from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, PostImages, Post


# class CommetForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['body']


# class PostImageForm(forms.Form):
#     Image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'latex']


class PostImageCreateForm(forms.ModelForm):
    class Meta:
        model = PostImages
        fields = ['image']
