from django.forms import ModelForm
from rabbit.models import *
from django import forms


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
        }


class ImgPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['img', 'title']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
        }


class LinkPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['link', 'title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'link': forms.TextInput(attrs={'placeholder': 'Write ur link', 'class': 'form-control'}),
        }

class WarrenForm(ModelForm):
    class Meta:
        model = Warren
        fields = ['name', 'description', 'profile_img', 'landscape_img']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Write a little description'}),
        }