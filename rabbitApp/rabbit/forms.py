from django.forms import ModelForm
from rabbit.models import *
from django import forms


class PostForm(ModelForm):
    warren = forms.ModelChoiceField(Warren.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ['description', 'title', 'warren']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
        }


class ImgPostForm(ModelForm):
    warren = forms.ModelChoiceField(Warren.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ['img', 'title', 'warren']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
        }


class LinkPostForm(ModelForm):
    warren = forms.ModelChoiceField(Warren.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ['link', 'title', 'warren']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'link': forms.TextInput(attrs={'placeholder': 'Write ur link', 'class': 'form-control'}),
        }


class WarrenForm(ModelForm):
    profile_img = forms.ImageField(required=False)
    landscape_img = forms.ImageField(required=False)

    class Meta:
        model = Warren
        fields = ['name', 'description', 'profile_img', 'landscape_img']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'description': forms.Textarea(attrs={'rows': '5', 'placeholder': 'Write a little description'}),
        }


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control','rows': '5','placeholder': 'What are your thoughts?'}),
        }