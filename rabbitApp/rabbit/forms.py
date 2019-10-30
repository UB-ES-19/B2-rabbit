from django.forms import ModelForm
from rabbit.models import Post
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
