from django.forms import ModelForm
from rabbit.models import DescriptionPost
from django import forms


class PostForm(ModelForm):
    class Meta:
        model = DescriptionPost
        fields = ['description', 'title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
        }
