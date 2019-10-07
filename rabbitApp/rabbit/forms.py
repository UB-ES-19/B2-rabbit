from django.forms import ModelForm
from rabbit.models import *
from django import forms


class PostForm(ModelForm):
    class Meta:
        model = DescriptionPost
        fields = ['description', 'title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
        }


class ImgPostForm(ModelForm):
    class Meta:
        model = ImgPost
        fields = ['img', 'title']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
        }