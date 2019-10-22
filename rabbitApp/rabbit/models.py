from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
import os


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

def get_image_filename(instance, filename):
    return "images/post/%s" % str(datetime.now()) + filename


class DescriptionPost(Post):
    description = models.TextField(max_length=255, blank=True)


class ImgPost(Post):
    img = models.FileField(upload_to=get_image_filename)


class LinkPost(Post):
    link = models.URLField()
