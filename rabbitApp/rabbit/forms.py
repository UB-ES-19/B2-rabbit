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
