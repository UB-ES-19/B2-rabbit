from django.forms import ModelForm
from rabbit.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'title', 'user']

